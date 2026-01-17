"""
Stochastic Stackelberg Game Model for Federal-Local Cost-Sharing in Flood Buyouts
==================================================================================

This module implements the three-level stochastic Stackelberg game model analyzing
equity implications of federal-local cost-sharing arrangements in flood buyout programs.

Building upon:
- Bier, V. M., Zhou, Y., & Du, H. (2019). Game-theoretic modeling of pre-disaster relocation.
- Zhou, Y. (2022). Pre-disaster relocation and agent-based model for flood disaster.

Author: [Your Name]
Date: January 2026
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize
from scipy.stats import genextreme
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import warnings


# =============================================================================
# Data Classes for Model Components
# =============================================================================

@dataclass
class ClimateScenario:
    """
    Represents a climate scenario (RCP pathway) with associated parameters.

    Attributes:
        name: Scenario identifier (e.g., 'RCP2.6', 'RCP4.5', 'RCP8.5')
        probability: Prior probability of this scenario
        slr_2100: Sea level rise by 2100 in meters
        a: Quadratic coefficient for SLR trajectory
        b: Linear coefficient for SLR trajectory
    """
    name: str
    probability: float
    slr_2100: float  # meters
    a: float = 0.0  # Quadratic coefficient
    b: float = 0.0  # Linear coefficient

    def __post_init__(self):
        """Calculate trajectory coefficients based on 2100 projection."""
        # Assuming quadratic trajectory: δ(t) = a*t² + b*t
        # With δ(0) = 0 and δ(80) = slr_2100 (assuming 2020-2100)
        T = 80  # years to 2100
        self.a = self.slr_2100 / (T ** 2)
        self.b = 0  # Simplified: purely quadratic growth

    def sea_level_rise(self, year: int) -> float:
        """Calculate sea level rise at given year (0 = base year)."""
        return self.a * (year ** 2) + self.b * year


@dataclass
class Household:
    """
    Represents a heterogeneous household in the model.

    Attributes:
        id: Unique identifier
        jurisdiction: Jurisdiction index
        house_value: Total market value ($)
        structure_value: Structure value for damage calculation ($)
        elevation: Property elevation (meters above sea level)
        discount_rate: Household-specific discount rate
        income_group: 'low' or 'high'
        relocation_cost: Total cost of relocation ($)
    """
    id: int
    jurisdiction: int
    house_value: float
    structure_value: float
    elevation: float
    discount_rate: float
    income_group: str
    relocation_cost: float = field(init=False)
    moving_cost: float = 50000  # Base moving cost
    psychic_cost: float = 100000  # Psychic cost of dislocation

    def __post_init__(self):
        self.relocation_cost = self.house_value + self.moving_cost + self.psychic_cost


@dataclass
class LocalGovernment:
    """
    Represents a local government (jurisdiction).

    Attributes:
        id: Jurisdiction identifier
        discount_rate: Local government discount rate
        tax_rate: Property tax rate
        tax_base_weight: Weight on tax base preservation (λ_j)
        admin_cost: Administrative cost of buyout program
        households: List of households in jurisdiction
    """
    id: int
    discount_rate: float = 0.06
    tax_rate: float = 0.015
    tax_base_weight: float = 0.2
    admin_cost: float = 100000
    households: List[Household] = field(default_factory=list)

    @property
    def median_house_value(self) -> float:
        """Calculate median house value in jurisdiction."""
        if not self.households:
            return 0
        values = [h.house_value for h in self.households]
        return np.median(values)

    @property
    def total_tax_base(self) -> float:
        """Calculate total property tax base."""
        return sum(h.house_value for h in self.households)


@dataclass
class FederalGovernment:
    """
    Federal government parameters.

    Attributes:
        discount_rate: Federal social discount rate
        budget: Total budget for buyout programs
        equity_threshold: Minimum equity ratio (θ)
        alpha_bounds: Bounds on cost-share ratio
    """
    discount_rate: float = 0.025
    budget: float = 1e9  # $1 billion
    equity_threshold: float = 0.8
    alpha_bounds: Tuple[float, float] = (0.5, 1.0)


# =============================================================================
# Flood Risk and Damage Model
# =============================================================================

class FloodRiskModel:
    """
    Models flood risk and expected damages under climate uncertainty.

    Based on Buchanan et al. (2016) approach for evolving flood frequencies.
    """

    def __init__(self,
                 gev_location: float = 1.5,
                 gev_scale: float = 0.3,
                 gev_shape: float = 0.1,
                 base_frequency: float = 0.01):
        """
        Initialize flood risk model.

        Args:
            gev_location: GEV location parameter (μ)
            gev_scale: GEV scale parameter (σ)
            gev_shape: GEV shape parameter (ξ)
            base_frequency: Base annual flood frequency (λ)
        """
        self.mu = gev_location
        self.sigma = gev_scale
        self.xi = gev_shape
        self.lambda_base = base_frequency

    def flood_probability(self,
                          elevation: float,
                          slr: float,
                          threshold_depth: float = 0.0) -> float:
        """
        Calculate annual flood probability for a property.

        Args:
            elevation: Property elevation (m)
            slr: Current sea level rise (m)
            threshold_depth: Minimum flood depth to count as flooding

        Returns:
            Annual probability of flooding
        """
        # Effective elevation accounting for SLR
        effective_elevation = elevation - slr

        if effective_elevation <= threshold_depth:
            return 1.0  # Already below water level

        # GEV exceedance probability
        if self.xi != 0:
            z = (effective_elevation - self.mu) / self.sigma
            if 1 + self.xi * z <= 0:
                return 1.0 if self.xi < 0 else 0.0
            prob = 1 - np.exp(-(1 + self.xi * z) ** (-1/self.xi))
        else:
            # Gumbel case (ξ = 0)
            z = (effective_elevation - self.mu) / self.sigma
            prob = 1 - np.exp(-np.exp(-z))

        return min(max(prob * self.lambda_base, 0), 1)

    def depth_damage_function(self, depth: float) -> float:
        """
        USACE depth-damage function for residential structures.

        Args:
            depth: Flood depth in meters

        Returns:
            Proportional damage to structure (0-1)
        """
        if depth <= 0:
            return 0.0
        elif depth < 0.3:  # 0-1 ft
            return 0.1 * (depth / 0.3)
        elif depth < 0.6:  # 1-2 ft
            return 0.1 + 0.15 * ((depth - 0.3) / 0.3)
        elif depth < 1.2:  # 2-4 ft
            return 0.25 + 0.20 * ((depth - 0.6) / 0.6)
        elif depth < 2.4:  # 4-8 ft
            return 0.45 + 0.25 * ((depth - 1.2) / 1.2)
        else:  # > 8 ft
            return min(0.70 + 0.05 * ((depth - 2.4) / 1.2), 1.0)

    def expected_annual_damage(self,
                               household: Household,
                               slr: float,
                               n_samples: int = 100) -> float:
        """
        Calculate expected annual flood damage for a household.

        Uses analytical approximation instead of full Monte Carlo for performance.

        Args:
            household: Household object
            slr: Current sea level rise
            n_samples: Number of Monte Carlo samples (reduced for performance)

        Returns:
            Expected annual damage in dollars
        """
        flood_prob = self.flood_probability(household.elevation, slr)

        if flood_prob < 1e-6:
            return 0.0

        # Analytical approximation: E[damage | flood] * P(flood)
        # For exponential depth distribution with scale=0.5,
        # compute expected damage ratio analytically
        # Using numerical integration over typical depth range
        expected_damage_ratio = 0.0
        depth_points = np.linspace(0.01, 5.0, 20)  # Sample depths
        scale = 0.5

        for depth in depth_points:
            # Exponential PDF: (1/scale) * exp(-depth/scale)
            pdf = (1/scale) * np.exp(-depth/scale)
            damage_ratio = self.depth_damage_function(depth)
            expected_damage_ratio += damage_ratio * pdf * (depth_points[1] - depth_points[0])

        return flood_prob * expected_damage_ratio * household.structure_value


# =============================================================================
# Homeowner Decision Model
# =============================================================================

class HomeownerModel:
    """
    Models individual homeowner relocation decisions.

    Following Bier et al. (2019) game-theoretic framework.
    """

    def __init__(self,
                 flood_model: FloodRiskModel,
                 scenarios: List[ClimateScenario],
                 planning_horizon: int = 80):
        """
        Initialize homeowner decision model.

        Args:
            flood_model: FloodRiskModel instance
            scenarios: List of climate scenarios
            planning_horizon: Years to consider (T)
        """
        self.flood_model = flood_model
        self.scenarios = scenarios
        self.T = planning_horizon
        # Cache for computed damage streams and NPVs
        self._damage_cache = {}
        self._npv_cache = {}
        self._npv_array_cache = {}  # Cache for precomputed NPV arrays
        # Precompute scenario-weighted damage factors
        self._precompute_damage_factors()

    def _precompute_damage_factors(self):
        """Precompute SLR values for each scenario and year for efficiency."""
        self._slr_by_scenario_year = {}
        for scenario in self.scenarios:
            for t in range(self.T):
                self._slr_by_scenario_year[(scenario.name, t)] = scenario.sea_level_rise(t)

    def _get_household_key(self, household: Household) -> tuple:
        """Generate a cache key for a household."""
        return (household.id, household.elevation, household.structure_value,
                household.discount_rate)

    def clear_caches(self):
        """Clear all caches to free memory."""
        self._damage_cache.clear()
        self._npv_cache.clear()
        self._npv_array_cache.clear()

    def expected_damage_stream(self,
                               household: Household,
                               start_year: int = 0) -> np.ndarray:
        """
        Calculate expected damage stream across all scenarios.
        Uses caching to avoid redundant calculations.

        Args:
            household: Household object
            start_year: Year to start calculation

        Returns:
            Array of expected annual damages by year
        """
        # Check cache first
        cache_key = (self._get_household_key(household), start_year)
        if cache_key in self._damage_cache:
            return self._damage_cache[cache_key]

        damages = np.zeros(self.T - start_year)

        for scenario in self.scenarios:
            prob = scenario.probability
            for t in range(start_year, self.T):
                # Use precomputed SLR values
                slr = self._slr_by_scenario_year[(scenario.name, t)]
                annual_damage = self.flood_model.expected_annual_damage(household, slr)
                damages[t - start_year] += prob * annual_damage

        # Store in cache
        self._damage_cache[cache_key] = damages
        return damages

    def npv_future_damages(self,
                           household: Household,
                           from_year: int) -> float:
        """
        Calculate NPV of future flood damages from a given year.
        Uses caching for efficiency.

        Args:
            household: Household object
            from_year: Year from which to calculate NPV

        Returns:
            NPV of expected future damages
        """
        # Check cache first
        cache_key = (self._get_household_key(household), from_year)
        if cache_key in self._npv_cache:
            return self._npv_cache[cache_key]

        damages = self.expected_damage_stream(household, from_year)
        discount_factors = np.array([
            1 / (1 + household.discount_rate) ** t
            for t in range(len(damages))
        ])
        result = np.sum(damages * discount_factors)

        # Store in cache
        self._npv_cache[cache_key] = result
        return result

    def _precompute_npvs_for_household(self, household: Household) -> np.ndarray:
        """
        Precompute all NPV values for a household to enable efficient search.

        Returns:
            Array of NPV values for each starting year
        """
        cache_key = self._get_household_key(household)
        if cache_key in self._npv_array_cache:
            return self._npv_array_cache[cache_key]

        # Compute full damage stream once
        full_damages = self.expected_damage_stream(household, 0)

        # Precompute discount factors
        discount_rate = household.discount_rate
        discount_factors = np.array([1 / (1 + discount_rate) ** t for t in range(self.T)])

        # Calculate NPV for each starting year efficiently using cumsum
        # NPV from year k = sum of damages[k:] * discount[0:T-k]
        # Use reverse cumsum for efficiency
        npvs = np.zeros(self.T)

        # Calculate from the end backwards for efficiency
        cumsum = 0.0
        for k in range(self.T - 1, -1, -1):
            cumsum = full_damages[k] * discount_factors[0] + cumsum / (1 + discount_rate)
            npvs[k] = cumsum

        # Cache the result
        self._npv_array_cache[cache_key] = npvs
        return npvs

    def optimal_relocation_year(self,
                                household: Household,
                                subsidy: float) -> int:
        """
        Find optimal relocation year for a household given subsidy.

        Implements Equation (4) from Bier et al. (2019).
        Uses precomputed NPVs for efficiency.

        Args:
            household: Household object
            subsidy: Offered subsidy amount

        Returns:
            Optimal relocation year (or T if never relocate)
        """
        net_relocation_cost = household.relocation_cost - subsidy

        if net_relocation_cost <= 0:
            return 0  # Relocate immediately

        # Get precomputed NPVs
        npvs = self._precompute_npvs_for_household(household)

        # Find first year where NPV of damages >= net relocation cost
        for k in range(self.T):
            if npvs[k] >= net_relocation_cost:
                return k

        return self.T  # Never relocate within horizon

    def is_free_rider(self, household: Household, subsidy: float) -> bool:
        """
        Determine if household is a free rider.

        A free rider relocates at the same time regardless of subsidy.

        Args:
            household: Household object
            subsidy: Offered subsidy amount

        Returns:
            True if household is a free rider
        """
        k_with_subsidy = self.optimal_relocation_year(household, subsidy)
        k_without_subsidy = self.optimal_relocation_year(household, 0)
        return k_with_subsidy == k_without_subsidy

    def minimum_subsidy_for_year(self,
                                 household: Household,
                                 target_year: int) -> float:
        """
        Calculate minimum subsidy to induce relocation by target year.

        Implements Equation (7) from Bier et al. (2019).

        Args:
            household: Household object
            target_year: Desired relocation year

        Returns:
            Minimum required subsidy
        """
        npv_damages = self.npv_future_damages(household, target_year)
        required_subsidy = household.relocation_cost - npv_damages
        return max(required_subsidy, 0)


# =============================================================================
# Local Government Decision Model
# =============================================================================

class LocalGovernmentModel:
    """
    Models local government buyout program decisions.
    """

    def __init__(self,
                 homeowner_model: HomeownerModel,
                 scenarios: List[ClimateScenario]):
        """
        Initialize local government model.

        Args:
            homeowner_model: HomeownerModel instance
            scenarios: List of climate scenarios
        """
        self.homeowner_model = homeowner_model
        self.scenarios = scenarios

    def aggregate_relocations(self,
                              local_gov: LocalGovernment,
                              subsidy: float) -> Dict:
        """
        Calculate aggregate relocation outcomes for a subsidy level.

        Args:
            local_gov: LocalGovernment object
            subsidy: Subsidy amount offered

        Returns:
            Dictionary with relocation statistics
        """
        relocations = {
            'total': 0,
            'low_income': 0,
            'high_income': 0,
            'free_riders': 0,
            'tax_base_loss': 0,
            'relocation_years': []
        }

        for h in local_gov.households:
            k_star = self.homeowner_model.optimal_relocation_year(h, subsidy)

            if k_star < self.homeowner_model.T:
                relocations['total'] += 1
                relocations['relocation_years'].append(k_star)
                relocations['tax_base_loss'] += h.house_value

                if h.income_group == 'low':
                    relocations['low_income'] += 1
                else:
                    relocations['high_income'] += 1

                if self.homeowner_model.is_free_rider(h, subsidy):
                    relocations['free_riders'] += 1

        return relocations

    def expected_local_cost(self,
                            local_gov: LocalGovernment,
                            subsidy: float,
                            alpha: float) -> float:
        """
        Calculate expected cost to local government.

        Args:
            local_gov: LocalGovernment object
            subsidy: Subsidy level
            alpha: Federal cost share ratio

        Returns:
            Expected present value of local government costs
        """
        relocations = self.aggregate_relocations(local_gov, subsidy)
        n_relocate = relocations['total']

        # Local cost share of buyouts
        buyout_cost = (1 - alpha) * subsidy * n_relocate

        # Administrative cost
        admin_cost = local_gov.admin_cost if n_relocate > 0 else 0

        # Tax base loss (PV)
        tax_base_loss = (local_gov.tax_base_weight *
                         local_gov.tax_rate *
                         relocations['tax_base_loss'] /
                         local_gov.discount_rate)

        # Expected disaster costs for non-relocated households
        disaster_cost = self._expected_disaster_cost(local_gov, subsidy)

        return buyout_cost + admin_cost + tax_base_loss + disaster_cost

    def _expected_disaster_cost(self,
                                local_gov: LocalGovernment,
                                subsidy: float) -> float:
        """Calculate expected disaster costs for non-relocated households.

        Optimized version: uses precomputed damage streams from homeowner model.
        """
        total_cost = 0
        local_discount_rate = local_gov.discount_rate
        T = self.homeowner_model.T

        # Precompute discount factors for local government
        local_discount_factors = np.array([1 / (1 + local_discount_rate) ** t for t in range(T)])

        for h in local_gov.households:
            k_star = self.homeowner_model.optimal_relocation_year(h, subsidy)

            if k_star < T:
                continue  # Household relocates

            # Use cached damage stream from homeowner model
            damages = self.homeowner_model.expected_damage_stream(h, 0)
            # Local gov bears 10% of infrastructure/emergency costs
            total_cost += 0.1 * np.sum(damages * local_discount_factors)

        return total_cost

    def optimal_subsidy(self,
                        local_gov: LocalGovernment,
                        alpha: float,
                        max_subsidy: float) -> Tuple[float, bool]:
        """
        Find optimal subsidy for local government.

        Uses grid search for faster optimization.

        Args:
            local_gov: LocalGovernment object
            alpha: Federal cost share ratio
            max_subsidy: Maximum allowable subsidy

        Returns:
            Tuple of (optimal subsidy, participation decision)
        """
        # Cost without participation
        cost_no_participation = self._expected_disaster_cost(local_gov, 0)

        # Use grid search instead of continuous optimization (faster)
        # Test subsidies at 10 levels from 0 to max
        subsidy_levels = np.linspace(0, max_subsidy, 11)
        costs = []

        for s in subsidy_levels:
            cost = self.expected_local_cost(local_gov, s, alpha)
            costs.append(cost)

        # Find minimum
        min_idx = np.argmin(costs)
        optimal_s = subsidy_levels[min_idx]
        cost_participation = costs[min_idx]

        # Participation decision
        participate = cost_participation < cost_no_participation

        return (optimal_s if participate else 0, participate)

    def participation_threshold(self,
                                local_gov: LocalGovernment,
                                max_subsidy: float) -> float:
        """
        Calculate critical alpha for participation.

        Args:
            local_gov: LocalGovernment object
            max_subsidy: Maximum subsidy

        Returns:
            Critical cost share ratio for participation
        """
        def net_benefit(alpha):
            _, participate = self.optimal_subsidy(local_gov, alpha, max_subsidy)
            if not participate:
                return 1  # High cost to encourage participation
            return -1  # Participates

        # Binary search for threshold
        low, high = 0.0, 1.0
        while high - low > 0.01:
            mid = (low + high) / 2
            _, participates = self.optimal_subsidy(local_gov, mid, max_subsidy)
            if participates:
                high = mid
            else:
                low = mid

        return high


# =============================================================================
# Federal Government Optimization
# =============================================================================

class FederalOptimizer:
    """
    Optimizes federal cost-sharing policy.
    """

    def __init__(self,
                 local_gov_model: LocalGovernmentModel,
                 federal_gov: FederalGovernment,
                 jurisdictions: List[LocalGovernment]):
        """
        Initialize federal optimizer.

        Args:
            local_gov_model: LocalGovernmentModel instance
            federal_gov: FederalGovernment object
            jurisdictions: List of local governments
        """
        self.local_model = local_gov_model
        self.federal = federal_gov
        self.jurisdictions = jurisdictions

    def evaluate_policy(self,
                        alpha: float,
                        max_subsidy: float) -> Dict:
        """
        Evaluate outcomes under a given federal policy.

        Args:
            alpha: Federal cost share ratio
            max_subsidy: Maximum subsidy cap

        Returns:
            Dictionary of outcomes
        """
        outcomes = {
            'alpha': alpha,
            'max_subsidy': max_subsidy,
            'total_federal_cost': 0,
            'total_relocations': 0,
            'low_income_relocations': 0,
            'high_income_relocations': 0,
            'participating_jurisdictions': 0,
            'free_riders': 0,
            'equity_ratio': 0,
            'jurisdiction_details': []
        }

        total_low = 0
        total_high = 0

        for j in self.jurisdictions:
            optimal_s, participates = self.local_model.optimal_subsidy(j, alpha, max_subsidy)

            if participates:
                outcomes['participating_jurisdictions'] += 1
                relocations = self.local_model.aggregate_relocations(j, optimal_s)

                federal_cost = alpha * optimal_s * relocations['total']
                outcomes['total_federal_cost'] += federal_cost
                outcomes['total_relocations'] += relocations['total']
                outcomes['low_income_relocations'] += relocations['low_income']
                outcomes['high_income_relocations'] += relocations['high_income']
                outcomes['free_riders'] += relocations['free_riders']

                # Count totals
                for h in j.households:
                    if h.income_group == 'low':
                        total_low += 1
                    else:
                        total_high += 1

                outcomes['jurisdiction_details'].append({
                    'id': j.id,
                    'subsidy': optimal_s,
                    'relocations': relocations
                })
            else:
                for h in j.households:
                    if h.income_group == 'low':
                        total_low += 1
                    else:
                        total_high += 1

        # Calculate equity ratio
        if total_low > 0 and total_high > 0:
            low_rate = outcomes['low_income_relocations'] / total_low
            high_rate = outcomes['high_income_relocations'] / total_high
            if high_rate > 0:
                outcomes['equity_ratio'] = low_rate / high_rate
            else:
                outcomes['equity_ratio'] = float('inf') if low_rate > 0 else 1.0
        else:
            outcomes['equity_ratio'] = 1.0

        return outcomes

    def optimize(self,
                 alpha_grid: np.ndarray = None,
                 subsidy_grid: np.ndarray = None) -> Dict:
        """
        Find optimal federal policy.

        Args:
            alpha_grid: Grid of alpha values to search
            subsidy_grid: Grid of max subsidy values to search

        Returns:
            Optimal policy and outcomes
        """
        if alpha_grid is None:
            alpha_grid = np.linspace(0.5, 1.0, 11)
        if subsidy_grid is None:
            subsidy_grid = np.linspace(100000, 500000, 9)

        best_outcome = None
        best_cost = float('inf')

        for alpha in alpha_grid:
            for max_s in subsidy_grid:
                outcomes = self.evaluate_policy(alpha, max_s)

                # Check constraints
                if outcomes['total_federal_cost'] > self.federal.budget:
                    continue
                if outcomes['equity_ratio'] < self.federal.equity_threshold:
                    continue

                if outcomes['total_federal_cost'] < best_cost:
                    best_cost = outcomes['total_federal_cost']
                    best_outcome = outcomes

        return best_outcome if best_outcome else self.evaluate_policy(0.75, 200000)


# =============================================================================
# Equity Analysis
# =============================================================================

class EquityAnalyzer:
    """
    Analyzes equity implications of buyout policies.
    """

    def __init__(self, homeowner_model: HomeownerModel):
        self.homeowner_model = homeowner_model

    def relocation_ratio_gap(self,
                             jurisdictions: List[LocalGovernment],
                             subsidy: float) -> float:
        """
        Calculate the Relocation Ratio Gap metric.

        RRG = (low_relocate/low_total) / (high_relocate/high_total)
        """
        low_relocate = 0
        low_total = 0
        high_relocate = 0
        high_total = 0

        for j in jurisdictions:
            for h in j.households:
                k_star = self.homeowner_model.optimal_relocation_year(h, subsidy)
                relocates = k_star < self.homeowner_model.T

                if h.income_group == 'low':
                    low_total += 1
                    if relocates:
                        low_relocate += 1
                else:
                    high_total += 1
                    if relocates:
                        high_relocate += 1

        if high_total == 0 or low_total == 0:
            return 1.0

        low_rate = low_relocate / low_total
        high_rate = high_relocate / high_total

        if high_rate == 0:
            return float('inf') if low_rate > 0 else 1.0

        return low_rate / high_rate

    def timing_gap(self,
                   jurisdictions: List[LocalGovernment],
                   subsidy: float) -> float:
        """
        Calculate average timing gap between income groups.

        Positive values indicate low-income relocates later.
        """
        low_years = []
        high_years = []

        for j in jurisdictions:
            for h in j.households:
                k_star = self.homeowner_model.optimal_relocation_year(h, subsidy)
                if k_star < self.homeowner_model.T:
                    if h.income_group == 'low':
                        low_years.append(k_star)
                    else:
                        high_years.append(k_star)

        if not low_years or not high_years:
            return 0.0

        return np.mean(low_years) - np.mean(high_years)

    def subsidy_gini(self,
                     jurisdictions: List[LocalGovernment],
                     subsidy: float) -> float:
        """
        Calculate Gini coefficient of subsidy distribution.
        """
        subsidies_received = []

        for j in jurisdictions:
            for h in j.households:
                k_star = self.homeowner_model.optimal_relocation_year(h, subsidy)
                if k_star < self.homeowner_model.T:
                    subsidies_received.append(subsidy)
                else:
                    subsidies_received.append(0)

        if not subsidies_received or sum(subsidies_received) == 0:
            return 0.0

        # Gini calculation
        sorted_subs = np.sort(subsidies_received)
        n = len(sorted_subs)
        cumulative = np.cumsum(sorted_subs)
        gini = (n + 1 - 2 * np.sum(cumulative) / cumulative[-1]) / n

        return gini

    def expected_damage_ratio(self,
                              jurisdictions: List[LocalGovernment],
                              subsidy: float) -> float:
        """
        Calculate ratio of expected damages by income group.

        Values > 1 indicate low-income bears more damage.
        Uses cached NPV values for efficiency.
        """
        low_damage = 0.0
        high_damage = 0.0

        for j in jurisdictions:
            for h in j.households:
                k_star = self.homeowner_model.optimal_relocation_year(h, subsidy)

                if k_star >= self.homeowner_model.T:
                    # Use cached NPV calculation instead of recalculating
                    total_damage = self.homeowner_model.npv_future_damages(h, 0)

                    if h.income_group == 'low':
                        low_damage += total_damage
                    else:
                        high_damage += total_damage

        if high_damage == 0:
            return float('inf') if low_damage > 0 else 1.0

        return low_damage / high_damage

    def comprehensive_analysis(self,
                               jurisdictions: List[LocalGovernment],
                               alpha_values: np.ndarray,
                               base_subsidy: float) -> Dict:
        """
        Perform comprehensive equity analysis across alpha values.
        """
        results = {
            'alpha': [],
            'rrg': [],
            'timing_gap': [],
            'gini': [],
            'damage_ratio': []
        }

        for alpha in alpha_values:
            # Adjust effective subsidy based on alpha
            # Higher alpha means local gov offers more
            effective_subsidy = base_subsidy * (1 + (alpha - 0.75) * 2)

            results['alpha'].append(alpha)
            results['rrg'].append(self.relocation_ratio_gap(jurisdictions, effective_subsidy))
            results['timing_gap'].append(self.timing_gap(jurisdictions, effective_subsidy))
            results['gini'].append(self.subsidy_gini(jurisdictions, effective_subsidy))
            results['damage_ratio'].append(self.expected_damage_ratio(jurisdictions, effective_subsidy))

        return results


# =============================================================================
# Simulation and Analysis
# =============================================================================

def create_sample_population(n_jurisdictions: int = 3,
                             households_per_jurisdiction: int = 100,
                             seed: int = 42) -> Tuple[List[LocalGovernment], List[ClimateScenario]]:
    """
    Create a sample population for simulation.

    Args:
        n_jurisdictions: Number of local governments
        households_per_jurisdiction: Households per jurisdiction
        seed: Random seed

    Returns:
        Tuple of (jurisdictions list, scenarios list)
    """
    np.random.seed(seed)

    # Create climate scenarios
    scenarios = [
        ClimateScenario("RCP2.6", 0.2, 0.4),
        ClimateScenario("RCP4.5", 0.5, 0.6),
        ClimateScenario("RCP8.5", 0.3, 1.0)
    ]

    jurisdictions = []
    household_id = 0

    for j in range(n_jurisdictions):
        # Vary jurisdiction characteristics
        tax_base_weight = 0.1 + 0.3 * np.random.random()
        admin_cost = 50000 + 150000 * np.random.random()

        local_gov = LocalGovernment(
            id=j,
            discount_rate=0.05 + 0.02 * np.random.random(),
            tax_rate=0.01 + 0.01 * np.random.random(),
            tax_base_weight=tax_base_weight,
            admin_cost=admin_cost
        )

        households = []
        for _ in range(households_per_jurisdiction):
            # Generate heterogeneous household
            house_value = np.random.lognormal(mean=12.5, sigma=0.5)  # ~$250K median

            # Income group based on house value
            median_val = np.exp(12.5)
            income_group = 'low' if house_value < median_val else 'high'

            # Discount rate varies by income (Bier et al. 2019)
            if income_group == 'low':
                discount_rate = 0.15 + 0.05 * np.random.random()  # 15-20%
            else:
                discount_rate = 0.08 + 0.06 * np.random.random()  # 8-14%

            # Elevation varies
            elevation = 1.0 + 2.0 * np.random.random()  # 1-3 meters

            h = Household(
                id=household_id,
                jurisdiction=j,
                house_value=house_value,
                structure_value=house_value * 0.7,
                elevation=elevation,
                discount_rate=discount_rate,
                income_group=income_group
            )
            households.append(h)
            household_id += 1

        local_gov.households = households
        jurisdictions.append(local_gov)

    return jurisdictions, scenarios


def run_simulation():
    """
    Run full simulation demonstrating the model.
    """
    print("=" * 70)
    print("Stochastic Stackelberg Game: Federal-Local Cost-Sharing Analysis")
    print("=" * 70)

    # Create population
    print("\n1. Creating sample population...")
    jurisdictions, scenarios = create_sample_population(
        n_jurisdictions=3,
        households_per_jurisdiction=100
    )

    total_households = sum(len(j.households) for j in jurisdictions)
    print(f"   - {len(jurisdictions)} jurisdictions")
    print(f"   - {total_households} total households")
    print(f"   - {len(scenarios)} climate scenarios")

    # Initialize models
    print("\n2. Initializing models...")
    flood_model = FloodRiskModel()
    homeowner_model = HomeownerModel(flood_model, scenarios, planning_horizon=80)
    local_gov_model = LocalGovernmentModel(homeowner_model, scenarios)

    federal_gov = FederalGovernment(
        discount_rate=0.025,
        budget=1e8,
        equity_threshold=0.7
    )

    federal_optimizer = FederalOptimizer(local_gov_model, federal_gov, jurisdictions)
    equity_analyzer = EquityAnalyzer(homeowner_model)

    # Analyze current policy (75/25 split)
    print("\n3. Analyzing current policy (α = 0.75)...")
    current_outcomes = federal_optimizer.evaluate_policy(0.75, 200000)

    print(f"\n   Current Policy Outcomes:")
    print(f"   - Total Federal Cost: ${current_outcomes['total_federal_cost']:,.0f}")
    print(f"   - Total Relocations: {current_outcomes['total_relocations']}")
    print(f"   - Low-Income Relocations: {current_outcomes['low_income_relocations']}")
    print(f"   - High-Income Relocations: {current_outcomes['high_income_relocations']}")
    print(f"   - Equity Ratio (RRG): {current_outcomes['equity_ratio']:.3f}")
    print(f"   - Free Riders: {current_outcomes['free_riders']}")

    # Compare different alpha values
    print("\n4. Comparative analysis of cost-share ratios...")
    alpha_values = [0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]

    print(f"\n   {'Alpha':<10} {'Federal Cost':<15} {'Relocations':<12} {'RRG':<8} {'Free Riders':<12}")
    print("   " + "-" * 55)

    for alpha in alpha_values:
        outcomes = federal_optimizer.evaluate_policy(alpha, 200000)
        print(f"   {alpha:<10.2f} ${outcomes['total_federal_cost']:>12,.0f} "
              f"{outcomes['total_relocations']:>10} {outcomes['equity_ratio']:>8.3f} "
              f"{outcomes['free_riders']:>10}")

    # Equity analysis
    print("\n5. Comprehensive equity analysis...")
    equity_results = equity_analyzer.comprehensive_analysis(
        jurisdictions,
        np.array(alpha_values),
        200000
    )

    print(f"\n   {'Alpha':<10} {'RRG':<10} {'Timing Gap':<12} {'Gini':<10}")
    print("   " + "-" * 42)

    for i, alpha in enumerate(equity_results['alpha']):
        print(f"   {alpha:<10.2f} {equity_results['rrg'][i]:<10.3f} "
              f"{equity_results['timing_gap'][i]:<12.2f} {equity_results['gini'][i]:<10.3f}")

    # Find optimal policy
    print("\n6. Optimizing federal policy...")
    optimal = federal_optimizer.optimize()

    if optimal:
        print(f"\n   Optimal Policy:")
        print(f"   - Cost Share Ratio (α*): {optimal['alpha']:.2f}")
        print(f"   - Maximum Subsidy: ${optimal['max_subsidy']:,.0f}")
        print(f"   - Total Federal Cost: ${optimal['total_federal_cost']:,.0f}")
        print(f"   - Equity Ratio: {optimal['equity_ratio']:.3f}")

    print("\n" + "=" * 70)
    print("Simulation complete.")
    print("=" * 70)

    return {
        'jurisdictions': jurisdictions,
        'scenarios': scenarios,
        'current_outcomes': current_outcomes,
        'optimal_policy': optimal,
        'equity_results': equity_results
    }


if __name__ == "__main__":
    results = run_simulation()
