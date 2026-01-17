"""
Real-World Parameters for Flood Buyout Cost-Sharing Model
=========================================================

This module contains empirically-grounded parameter values from academic literature,
government reports, and official data sources.

Data Sources:
- FEMA HMGP Cost-Sharing: https://www.fema.gov/hmgp-appeal-categories/cost-sharing
- USACE Depth-Damage Functions: https://planning.erdc.dren.mil/toolbox/library/IWRServer/92-R-3.pdf
- IPCC Sea Level Rise Projections: https://www.ipcc.ch/srocc/chapter/chapter-4-sea-level-rise-and-implications-for-low-lying-islands-coasts-and-communities/
- Discount Rates: Warner & Pleeter (2001), Newell & Siikamaki (2014)
- NYC Flood Zone Data: https://www.nyc.gov/site/floodmaps/maps/overview.page

Author: [Your Name]
Date: January 2026
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# =============================================================================
# FEMA AND GOVERNMENT POLICY PARAMETERS
# =============================================================================

@dataclass
class FEMAParameters:
    """
    FEMA Hazard Mitigation Grant Program (HMGP) parameters.

    Sources:
    - FEMA Cost Sharing Policy: https://www.fema.gov/hmgp-appeal-categories/cost-sharing
    - GAO-25-107603 Report on HMGP funding
    - Congress.gov CRS Report IN11911
    """
    # Standard cost-sharing ratios
    federal_share_standard: float = 0.75  # 75% federal share (standard HMGP)
    federal_share_enhanced: float = 0.90  # Up to 90% for Enhanced Mitigation Plan
    federal_share_small_impoverished: float = 1.00  # 100% for small impoverished communities

    # Program statistics (as of 2024)
    average_obligate_time_months: float = 19.5  # Average time to obligate HMGP funding
    cost_benefit_ratio_low: float = 4.0  # $4-6 saved per $1 invested (conservative)
    cost_benefit_ratio_high: float = 6.0
    nibs_benefit_ratio_low: float = 5.0  # NIBS estimates $5-9 saved per $1
    nibs_benefit_ratio_high: float = 9.0

    # Budget context (FY2015-2024)
    total_disaster_appropriations_billion: float = 448.0  # Total disaster assistance
    hmgp_cost_share_budget_billion: float = 1.1  # CDBG-MIT funds for HMGP cost share

    # Buyout program outcomes
    total_buyout_counties: int = 1100  # Counties with buyout programs (49 states)
    total_relocated_residents: int = 70000  # Residents who moved following buyouts
    flood_risk_reduction_percent: float = 0.63  # Average 63% decrease in flood risk


@dataclass
class DiscountRateParameters:
    """
    Empirically-estimated discount rates by income/demographic group.

    Sources:
    - Warner & Pleeter (2001) "The Personal Discount Rate: Evidence from
      Military Downsizing Programs" American Economic Review
    - Newell & Siikamaki (2014) "Nudging Energy Efficiency Behavior"
      Journal of Environmental Economics and Management
    - Hausman (1979) "Individual Discount Rates and the Purchase and
      Utilization of Energy-Using Durables" Bell Journal of Economics
    - Bier et al. (2019) - used 12% for residents in game-theoretic model
    """
    # Federal/Government discount rates
    federal_social_discount_rate: float = 0.025  # 2.5% - CBO practice
    federal_discount_rate_omb_real: float = 0.02  # 2% real rate (OMB Circular A-4)
    federal_discount_rate_omb_nominal: float = 0.07  # 7% opportunity cost of capital

    # Local government discount rates (higher due to political cycles)
    local_government_low: float = 0.05  # 5% for long-term planning
    local_government_high: float = 0.08  # 8% for politically-constrained

    # Household discount rates by income (Warner & Pleeter 2001)
    # Key finding: "90 percent of enlisted personnel chose the lump sum,
    # implying personal discount rates of at least 17 percent"
    household_high_income: float = 0.10  # ~10% for high-income households
    household_median_income: float = 0.15  # ~15% for median income
    household_low_income: float = 0.20  # ~20% for low-income (Hausman 1979)
    household_credit_constrained: float = 0.25  # Up to 25% for credit-constrained

    # Hyperbolic discounting parameters (quasi-hyperbolic β-δ model)
    # β captures present bias (β < 1 means present-biased)
    hyperbolic_beta_low: float = 0.70  # Strong present bias
    hyperbolic_beta_high: float = 0.95  # Weak present bias

    # Bier et al. (2019) base case parameters
    bier_resident_discount_rate: float = 0.12  # 12% in base case
    bier_government_discount_rate: float = 0.05  # 5% in base case


# =============================================================================
# CLIMATE AND SEA LEVEL RISE PARAMETERS
# =============================================================================

@dataclass
class ClimateProjections:
    """
    IPCC sea level rise projections by RCP/SSP scenario.

    Sources:
    - IPCC AR5 (2013) - RCP scenarios
    - IPCC SROCC (2019) - Updated with MISI
    - IPCC AR6 (2021) - SSP scenarios
    - NASA Sea Level Projection Tool: https://sealevel.nasa.gov/ipcc-ar6-sea-level-projection-tool
    """

    # IPCC AR5/SROCC RCP Scenarios - Global Mean Sea Level Rise by 2100 (meters)
    # Format: (median, likely_range_low, likely_range_high)
    rcp26_2100: Tuple[float, float, float] = (0.43, 0.29, 0.59)  # Optimistic
    rcp45_2100: Tuple[float, float, float] = (0.53, 0.36, 0.71)  # Moderate
    rcp85_2100: Tuple[float, float, float] = (0.84, 0.61, 1.10)  # Pessimistic/BAU

    # IPCC AR6 SSP Scenarios (slightly higher projections)
    ssp126_2100: Tuple[float, float, float] = (0.44, 0.32, 0.62)
    ssp245_2100: Tuple[float, float, float] = (0.56, 0.44, 0.76)
    ssp585_2100: Tuple[float, float, float] = (0.77, 0.63, 1.01)

    # Scenario probabilities (subjective - for stochastic model)
    # Based on current emissions trajectory being between RCP4.5 and RCP8.5
    prob_optimistic: float = 0.15  # RCP 2.6 / SSP1-2.6
    prob_moderate: float = 0.50   # RCP 4.5 / SSP2-4.5
    prob_pessimistic: float = 0.35  # RCP 8.5 / SSP5-8.5

    # Expert survey estimates (Bamber et al. 2019, Nature Clim. Change)
    # "Under RCP 2.6, experts projected likely GMSL rise of 0.30–0.65 m by 2100"
    expert_rcp26_likely: Tuple[float, float] = (0.30, 0.65)
    expert_rcp85_likely: Tuple[float, float] = (0.62, 1.38)

    # Regional amplification factors (US East Coast experiences higher SLR)
    # New York area experiences ~1.2-1.5x global average
    nyc_amplification_factor: float = 1.3

    # Current observed rate (for calibration)
    current_rate_mm_per_year: float = 3.7  # Global average 2006-2018
    nyc_rate_mm_per_year: float = 4.4  # NYC Battery tide gauge


@dataclass
class FloodFrequencyParameters:
    """
    Flood frequency parameters based on Buchanan et al. (2016) methodology.

    Sources:
    - Buchanan et al. (2016) "Allowances for evolving coastal flood risk
      under uncertain local sea-level rise" Climatic Change
    - Kopp et al. (2014) "Probabilistic 21st and 22nd century sea-level
      projections at a global network of tide-gauge sites"
    - FEMA Flood Insurance Rate Maps
    """

    # GEV distribution parameters for storm surge (NYC example)
    # Based on FEMA flood study data
    nyc_gev_location: float = 1.04  # Location parameter (meters NAVD88)
    nyc_gev_scale: float = 0.28     # Scale parameter
    nyc_gev_shape: float = 0.09     # Shape parameter (positive = heavy tail)

    # Return period flood heights (meters above MHHW) - NYC Battery
    nyc_10yr_flood: float = 1.17
    nyc_100yr_flood: float = 2.25
    nyc_500yr_flood: float = 2.87

    # Flood zone classifications (FEMA)
    zone_ve_desc: str = "Coastal high hazard (velocity zone)"
    zone_ae_desc: str = "100-year floodplain (1% annual chance)"
    zone_ao_desc: str = "Shallow flooding 1-3 feet"
    zone_x_desc: str = "500-year floodplain (0.2% annual chance)"


# =============================================================================
# DEPTH-DAMAGE FUNCTIONS (USACE)
# =============================================================================

@dataclass
class USACEDepthDamage:
    """
    USACE residential depth-damage functions.

    Sources:
    - USACE (2003) "Economic Guidance Memorandum 04-01"
    - USACE IWR Report 92-R-3 "Catalog of Residential Depth-Damage Functions"
    - FEMA Hazus-MH Technical Manual
    """

    # One-story residential structure, no basement
    # Format: (depth_ft, percent_damage)
    # Source: USACE Galveston District depth-damage curves
    one_story_no_basement: Dict[float, float] = field(default_factory=lambda: {
        -2.0: 0.00,   # 2 ft below first floor
        -1.0: 0.00,
        0.0: 0.00,    # At first floor level
        0.5: 0.08,    # 6 inches
        1.0: 0.14,    # 1 foot
        2.0: 0.23,    # 2 feet
        3.0: 0.31,    # 3 feet
        4.0: 0.39,    # 4 feet
        5.0: 0.45,    # 5 feet
        6.0: 0.50,    # 6 feet
        7.0: 0.55,
        8.0: 0.59,
        9.0: 0.62,
        10.0: 0.65,
        12.0: 0.69,
        14.0: 0.72,
        16.0: 0.75,
    })

    # Two-story residential structure, no basement
    two_story_no_basement: Dict[float, float] = field(default_factory=lambda: {
        -2.0: 0.00,
        -1.0: 0.00,
        0.0: 0.00,
        0.5: 0.06,
        1.0: 0.10,
        2.0: 0.17,
        3.0: 0.23,
        4.0: 0.29,
        5.0: 0.34,
        6.0: 0.38,
        7.0: 0.42,
        8.0: 0.45,
        9.0: 0.48,
        10.0: 0.51,
        12.0: 0.56,
        14.0: 0.60,
        16.0: 0.64,
    })

    # Content damage (typically higher at shallow depths)
    content_damage: Dict[float, float] = field(default_factory=lambda: {
        0.0: 0.00,
        0.5: 0.15,
        1.0: 0.25,
        2.0: 0.40,
        3.0: 0.52,
        4.0: 0.62,
        5.0: 0.70,
        6.0: 0.76,
        8.0: 0.85,
        10.0: 0.90,
    })

    def interpolate_damage(self,
                          depth_ft: float,
                          structure_type: str = 'one_story_no_basement') -> float:
        """Interpolate damage percentage for given depth."""
        if structure_type == 'one_story_no_basement':
            curve = self.one_story_no_basement
        elif structure_type == 'two_story_no_basement':
            curve = self.two_story_no_basement
        else:
            curve = self.content_damage

        depths = sorted(curve.keys())
        if depth_ft <= depths[0]:
            return curve[depths[0]]
        if depth_ft >= depths[-1]:
            return curve[depths[-1]]

        # Linear interpolation
        for i in range(len(depths) - 1):
            if depths[i] <= depth_ft <= depths[i+1]:
                d0, d1 = depths[i], depths[i+1]
                p0, p1 = curve[d0], curve[d1]
                return p0 + (p1 - p0) * (depth_ft - d0) / (d1 - d0)

        return 0.0


# =============================================================================
# PROPERTY AND RELOCATION COST PARAMETERS
# =============================================================================

@dataclass
class PropertyParameters:
    """
    Property value and relocation cost parameters.

    Sources:
    - PropertyShark NYC Flood Zone Analysis (2023)
    - American Moving & Storage Association
    - NRI Relocation corporate relocation costs (2025)
    - Bishop (2007), Kennan & Walker (2011) migration literature
    """

    # NYC/Brooklyn property values by flood zone (2023 data)
    # Source: https://www.propertyshark.com/Real-Estate-Reports/2023/10/16/nyc-flood-zones
    brooklyn_median_flood_zone_2023: float = 815000  # Median in flood zones
    brooklyn_median_non_flood_2023: float = 1005000  # Median outside flood zones
    brooklyn_flood_discount: float = 190000  # $190K lower in flood zones

    # Red Hook specific (gentrifying flood-prone neighborhood)
    red_hook_flood_zone_median: float = 2488000
    red_hook_price_change_pct: float = 2.79  # 279% increase since 2012

    # National property values (for comparison)
    us_median_home_value_2024: float = 420000

    # Structure value as fraction of total
    structure_value_fraction: float = 0.70  # 70% structure, 30% land

    # Moving costs (2024 data)
    # Source: American Moving & Storage Association, NerdWallet
    local_move_avg: float = 1714  # Within same city
    local_move_range: Tuple[float, float] = (883, 2556)
    long_distance_avg: float = 4500  # >1000 miles
    long_distance_range: Tuple[float, float] = (2700, 10000)
    full_service_avg: float = 9060

    # Corporate relocation costs (homeowner with sale)
    # Source: NRI Relocation 2025
    corporate_relocation_no_bvo: float = 45500
    corporate_relocation_with_bvo: float = 93000

    # Psychic/non-monetary costs of relocation
    # Source: Migration economics literature (Bishop 2007, Kennan & Walker 2011)
    # Estimates range from $50,000 to $500,000 in utility terms
    psychic_cost_low: float = 50000
    psychic_cost_median: float = 150000
    psychic_cost_high: float = 300000

    # Total relocation cost = property value + moving + psychic + transaction
    # Bier et al. (2019) used $300,000-$750,000 range
    bier_relocation_cost_low: float = 300000
    bier_relocation_cost_high: float = 750000


@dataclass
class BrooklynCaseStudyData:
    """
    Brooklyn, NY case study parameters (from proposal - 3 zip codes).

    Zip codes: 11234 (Bergen Beach), 11235 (Sheepshead Bay), 11236 (Canarsie)

    Sources:
    - Zhou (2022) dissertation
    - Zillow ZTRAX data (archived)
    - FEMA Flood Insurance Rate Maps
    """

    zip_codes: List[str] = field(default_factory=lambda: ['11234', '11235', '11236'])

    # Sample characteristics
    n_single_family_homes: int = 1143  # One-story single-family (from proposal)

    # Elevation distribution (meters above sea level)
    elevation_min: float = 0.5
    elevation_max: float = 4.0
    elevation_mean: float = 2.0

    # Property value distribution (based on NYC data)
    house_value_mean: float = 650000
    house_value_std: float = 250000
    house_value_min: float = 300000
    house_value_max: float = 1500000

    # Income mix (proxy from house values)
    pct_low_income: float = 0.45  # Below median
    pct_high_income: float = 0.55  # Above median

    # Flood zone distribution
    pct_in_100yr_floodplain: float = 0.35
    pct_in_500yr_floodplain: float = 0.25
    pct_outside_floodplain: float = 0.40


# =============================================================================
# EXPANDED REGIONAL CASE STUDY DATA
# =============================================================================

@dataclass
class StatenIslandCaseStudyData:
    """
    Staten Island, NY case study - significantly impacted by Hurricane Sandy.

    Sources:
    - NYC Build It Back Program data
    - NY Governor's Office of Storm Recovery
    - PropertyShark Staten Island flood zone analysis (2023)
    - FEMA Sandy Claims Data
    """

    zip_codes: List[str] = field(default_factory=lambda: [
        '10306',  # New Dorp, Midland Beach
        '10307',  # Tottenville
        '10308',  # Great Kills
        '10309',  # Charleston
        '10312',  # Annadale, Eltingville
        '10314',  # Bull's Head, Westerleigh
    ])

    # Sample characteristics - Staten Island has more single-family homes
    n_single_family_homes: int = 2850

    # Elevation distribution (meters) - lower than Brooklyn
    elevation_min: float = 0.3
    elevation_max: float = 5.5
    elevation_mean: float = 1.8

    # Property values (2023) - lower than Brooklyn
    house_value_mean: float = 580000
    house_value_std: float = 180000
    house_value_min: float = 280000
    house_value_max: float = 1200000

    # Staten Island has higher homeownership, more working-class
    pct_low_income: float = 0.52
    pct_high_income: float = 0.48

    # Flood zone distribution - higher flood exposure
    pct_in_100yr_floodplain: float = 0.42
    pct_in_500yr_floodplain: float = 0.28
    pct_outside_floodplain: float = 0.30

    # Hurricane Sandy impact
    sandy_damaged_homes: int = 12500
    sandy_buyout_participants: int = 326
    sandy_buyout_avg_price: float = 310000


@dataclass
class QueensCaseStudyData:
    """
    Queens, NY case study - Rockaway Peninsula and Howard Beach.

    Sources:
    - NYC Planning Flood Resilience Zoning
    - PropertyShark Queens analysis (2023)
    - FEMA Sandy Claims Data
    - Rebuild by Design studies
    """

    zip_codes: List[str] = field(default_factory=lambda: [
        '11691',  # Far Rockaway
        '11692',  # Arverne
        '11693',  # Far Rockaway
        '11694',  # Rockaway Park
        '11695',  # Far Rockaway
        '11414',  # Howard Beach
        '11693',  # Broad Channel
    ])

    n_single_family_homes: int = 3200

    # Rockaway is a narrow peninsula - very flood exposed
    elevation_min: float = 0.2
    elevation_max: float = 3.5
    elevation_mean: float = 1.5

    # Property values - varied (Rockaway gentrifying, Howard Beach stable)
    house_value_mean: float = 520000
    house_value_std: float = 220000
    house_value_min: float = 250000
    house_value_max: float = 1400000

    # More diverse income distribution
    pct_low_income: float = 0.58
    pct_high_income: float = 0.42

    # Very high flood exposure
    pct_in_100yr_floodplain: float = 0.65
    pct_in_500yr_floodplain: float = 0.20
    pct_outside_floodplain: float = 0.15

    # Hurricane Sandy impact
    sandy_damaged_homes: int = 8900
    sandy_rebuild_participants: int = 2100


@dataclass
class LowerManhattanCaseStudyData:
    """
    Lower Manhattan, NY case study - Financial District, Battery Park City.

    Sources:
    - NYC Planning Lower Manhattan Coastal Resiliency Project
    - PropertyShark Manhattan analysis (2023)
    - NYC Economic Development Corporation
    """

    zip_codes: List[str] = field(default_factory=lambda: [
        '10004',  # Financial District
        '10005',  # Financial District
        '10006',  # Financial District
        '10007',  # City Hall
        '10038',  # South Street Seaport
        '10280',  # Battery Park City
        '10282',  # Battery Park City
    ])

    # Fewer single-family, more commercial/condo - using condo units
    n_residential_units: int = 15000
    n_single_family_equivalent: int = 1500  # For comparison

    # Elevation - reclaimed land, very low
    elevation_min: float = 0.5
    elevation_max: float = 4.0
    elevation_mean: float = 2.0

    # Very high property values
    house_value_mean: float = 1850000
    house_value_std: float = 750000
    house_value_min: float = 600000
    house_value_max: float = 8000000

    # Mostly high income
    pct_low_income: float = 0.15
    pct_high_income: float = 0.85

    # Moderate flood exposure (major infrastructure investments)
    pct_in_100yr_floodplain: float = 0.45
    pct_in_500yr_floodplain: float = 0.30
    pct_outside_floodplain: float = 0.25

    # Economic exposure - mostly commercial
    commercial_property_value_billions: float = 85.0


@dataclass
class HoustonCaseStudyData:
    """
    Houston/Harris County, TX case study - Hurricane Harvey focus.

    Sources:
    - Harris County Flood Control District
    - Texas General Land Office Harvey recovery data
    - Rice University Kinder Institute Houston housing studies
    - FEMA Harvey Individual Assistance data
    """

    zip_codes: List[str] = field(default_factory=lambda: [
        '77024',  # Memorial
        '77079',  # Energy Corridor
        '77096',  # Meyerland
        '77025',  # Braeswood
        '77035',  # Meyerland South
        '77045',  # South Park
        '77051',  # Sunnyside
        '77033',  # South Acres
        '77061',  # Gulfgate
        '77087',  # Eastwood
        '77012',  # Magnolia Park
        '77547',  # Galena Park
    ])

    n_single_family_homes: int = 8500

    # Houston is flat and low-lying
    elevation_min: float = 5.0  # meters above sea level
    elevation_max: float = 15.0
    elevation_mean: float = 9.0

    # Property values (2023) - more affordable than NYC
    house_value_mean: float = 285000
    house_value_std: float = 175000
    house_value_min: float = 85000
    house_value_max: float = 1200000

    # Higher proportion low-income
    pct_low_income: float = 0.55
    pct_high_income: float = 0.45

    # Very high flood exposure
    pct_in_100yr_floodplain: float = 0.38
    pct_in_500yr_floodplain: float = 0.32
    pct_outside_floodplain: float = 0.30

    # Hurricane Harvey impact (2017)
    harvey_flooded_homes: int = 154000
    harvey_federal_assistance_billion: float = 12.5
    harvey_buyout_program_homes: int = 3500
    harvey_avg_buyout_price: float = 195000

    # Harris County specific
    harris_county_population: int = 4700000
    harris_county_repetitive_loss_properties: int = 8700

    # Discount rates may be different in TX
    texas_no_state_income_tax: bool = True


@dataclass
class MiamiDadeCaseStudyData:
    """
    Miami-Dade County, FL case study - sea level rise hotspot.

    Sources:
    - Miami-Dade County Sea Level Rise Strategy
    - Florida DEP Sea Level Rise data
    - Zillow Miami flood zone analysis
    - University of Miami RSMAS climate studies
    - NOAA Southeast Florida Sea Level Rise projections
    """

    zip_codes: List[str] = field(default_factory=lambda: [
        '33109',  # Fisher Island
        '33139',  # Miami Beach
        '33140',  # Miami Beach
        '33141',  # Miami Beach North
        '33154',  # Bay Harbor Islands
        '33180',  # Aventura
        '33030',  # Homestead
        '33032',  # Florida City
        '33033',  # Leisure City
        '33157',  # Perrine
        '33176',  # Kendall
        '33186',  # Kendall South
    ])

    n_single_family_homes: int = 6200

    # South Florida is extremely flat and low
    elevation_min: float = 0.3
    elevation_max: float = 4.5
    elevation_mean: float = 1.5

    # Property values - wide range from Homestead to Miami Beach
    house_value_mean: float = 485000
    house_value_std: float = 350000
    house_value_min: float = 150000
    house_value_max: float = 5000000

    # High inequality in Miami-Dade
    pct_low_income: float = 0.48
    pct_high_income: float = 0.52

    # Extreme flood exposure
    pct_in_100yr_floodplain: float = 0.52
    pct_in_500yr_floodplain: float = 0.28
    pct_outside_floodplain: float = 0.20

    # Sea level rise is accelerating here
    local_slr_rate_mm_per_year: float = 9.0  # Higher than global average
    projected_slr_2060_meters: float = 0.53  # NOAA Intermediate projection

    # Unique factors
    porous_limestone_aquifer: bool = True  # Can't build seawalls
    king_tide_flooding_days_2023: int = 12

    # Insurance crisis
    avg_flood_insurance_premium: float = 4200
    citizens_property_policies: int = 1400000  # State insurer of last resort


@dataclass
class NewOrleansCaseStudyData:
    """
    New Orleans/Orleans Parish, LA case study - post-Katrina focus.

    Sources:
    - NOLA.gov Road Home Program data
    - Louisiana Office of Community Development
    - Greater New Orleans Community Data Center
    - FEMA Katrina/Isaac recovery data
    - Tulane/LSU Coastal Studies
    """

    zip_codes: List[str] = field(default_factory=lambda: [
        '70112',  # CBD/Warehouse District
        '70113',  # Central City
        '70116',  # French Quarter/Marigny
        '70117',  # Bywater/St. Claude
        '70119',  # Mid-City
        '70122',  # Gentilly
        '70124',  # Lakeview
        '70126',  # New Orleans East
        '70127',  # New Orleans East
        '70128',  # New Orleans East
        '70129',  # Village de L'Est
        '70131',  # Algiers
    ])

    n_single_family_homes: int = 5400

    # Much of New Orleans is below sea level
    elevation_min: float = -2.0  # Below sea level
    elevation_max: float = 3.0
    elevation_mean: float = 0.5

    # Property values - still recovering from Katrina
    house_value_mean: float = 265000
    house_value_std: float = 165000
    house_value_min: float = 65000
    house_value_max: float = 950000

    # High proportion low-income
    pct_low_income: float = 0.62
    pct_high_income: float = 0.38

    # Protected by levees but still high risk
    pct_in_100yr_floodplain: float = 0.75  # Most of city
    pct_in_500yr_floodplain: float = 0.15
    pct_outside_floodplain: float = 0.10

    # Hurricane Katrina impact (2005)
    katrina_flooded_homes: int = 134000
    katrina_road_home_grants: int = 130000
    katrina_avg_road_home_grant: float = 65000

    # Repetitive loss - major problem
    repetitive_loss_properties: int = 5500
    severe_repetitive_loss: int = 1100

    # Subsidence adds to flood risk
    annual_subsidence_mm: float = 8.0

    # Post-Katrina buyouts
    katrina_buyout_areas: List[str] = field(default_factory=lambda: [
        'Lower 9th Ward (partial)',
        'New Orleans East (partial)',
        'Lakeview (limited)',
    ])


@dataclass
class NorfolkVACaseStudyData:
    """
    Norfolk/Hampton Roads, VA case study - military installations and chronic flooding.

    Sources:
    - City of Norfolk Resilience Strategy
    - NOAA Norfolk Tide Gauge (longest record on East Coast)
    - Hampton Roads Planning District Commission
    - Old Dominion University Sea Level Rise studies
    """

    zip_codes: List[str] = field(default_factory=lambda: [
        '23503',  # Ocean View
        '23505',  # Larchmont
        '23508',  # Ghent
        '23510',  # Downtown
        '23513',  # Campostella
        '23518',  # East Ocean View
        '23523',  # Berkley
        '23551',  # Naval Station Norfolk
    ])

    n_single_family_homes: int = 3100

    # Low-lying coastal area with land subsidence
    elevation_min: float = 0.3
    elevation_max: float = 4.0
    elevation_mean: float = 1.5

    # Property values - moderate
    house_value_mean: float = 245000
    house_value_std: float = 95000
    house_value_min: float = 95000
    house_value_max: float = 650000

    # Mixed income with significant military presence
    pct_low_income: float = 0.50
    pct_high_income: float = 0.50

    # Very high flood exposure
    pct_in_100yr_floodplain: float = 0.48
    pct_in_500yr_floodplain: float = 0.25
    pct_outside_floodplain: float = 0.27

    # Chronic flooding
    sunny_day_flood_events_2023: int = 14
    relative_slr_rate_mm_per_year: float = 5.1  # Includes subsidence

    # Military significance
    naval_station_norfolk_value_billion: float = 12.0
    military_personnel: int = 80000


@dataclass
class CharlestonSCCaseStudyData:
    """
    Charleston, SC case study - historic city with increasing flood risk.

    Sources:
    - City of Charleston Flooding & Sea Level Rise Strategy
    - College of Charleston Lowcountry Hazards Center
    - SC Sea Grant Consortium
    - NOAA Charleston Harbor tide gauge
    """

    zip_codes: List[str] = field(default_factory=lambda: [
        '29401',  # Downtown/Historic District
        '29403',  # Charleston Neck
        '29405',  # North Charleston
        '29407',  # West Ashley
        '29412',  # James Island
        '29414',  # West Ashley South
        '29455',  # Johns Island
    ])

    n_single_family_homes: int = 2600

    # Historic peninsula is very low
    elevation_min: float = 0.5
    elevation_max: float = 6.0
    elevation_mean: float = 2.5

    # Property values - historic homes command premium
    house_value_mean: float = 425000
    house_value_std: float = 285000
    house_value_min: float = 120000
    house_value_max: float = 2500000

    pct_low_income: float = 0.42
    pct_high_income: float = 0.58

    # High flood exposure
    pct_in_100yr_floodplain: float = 0.55
    pct_in_500yr_floodplain: float = 0.22
    pct_outside_floodplain: float = 0.23

    # Chronic flooding increasing
    flood_days_2023: int = 89  # Up from ~5 in 1970s
    projected_flood_days_2045: int = 180

    # Historic preservation concerns
    historic_properties_in_flood_zone: int = 3500


# =============================================================================
# LOCAL GOVERNMENT PARAMETERS
# =============================================================================

@dataclass
class LocalGovernmentParameters:
    """
    Local government fiscal and behavioral parameters.

    Sources:
    - Census of Governments
    - NYC Department of Finance property tax data
    - Slavikova (2018) on crowding-out effects
    """

    # Property tax rates
    nyc_property_tax_rate: float = 0.0089  # ~0.89% of assessed value
    nyc_assessment_ratio: float = 0.06  # 6% for Class 1 (residential)
    effective_tax_rate_nyc: float = 0.0089 * 0.06 / 0.45  # Adjusted for assessment
    national_median_property_tax_rate: float = 0.011  # 1.1%

    # Administrative costs for buyout programs
    admin_cost_per_program_low: float = 50000
    admin_cost_per_program_high: float = 200000
    admin_cost_per_property: float = 5000  # Per-property processing

    # Tax base preservation weight (λ in model)
    # Higher values = more concerned about losing tax base
    lambda_low: float = 0.1   # Low priority on tax base
    lambda_median: float = 0.25
    lambda_high: float = 0.5  # High priority (fiscally stressed)

    # Time to process buyouts (from FEMA data)
    federal_funded_time_years: float = 1.625  # 19.5 months
    state_local_funded_time_years: float = 0.5  # 2-3 years faster


# =============================================================================
# EQUITY BASELINE DATA
# =============================================================================

@dataclass
class EquityBaselineData:
    """
    Baseline data on equity in buyout programs.

    Sources:
    - Elliott et al. (2021) "Racial inequities in the federal buyout of
      flood-prone homes" Socius
    - Hazards Center/Natural Hazards Center reports
    """

    # Key finding from Elliott et al. (2021)
    # "buyout funding is disproportionately allocated to wealthier, white communities"

    # Observed disparities in buyout participation
    white_participation_rate: float = 0.65  # Approximate from literature
    minority_participation_rate: float = 0.45

    # Income-based disparities
    high_income_buyout_rate: float = 0.70
    low_income_buyout_rate: float = 0.50

    # Timing disparities (low-income wait longer)
    avg_wait_time_high_income_months: float = 18
    avg_wait_time_low_income_months: float = 28

    # Out-of-pocket burden
    # "if there's a 25% match requirement, they just get 25% less"
    match_burden_effective_reduction: float = 0.25


# =============================================================================
# COMPLETE PARAMETER SET FOR SIMULATION
# =============================================================================

def get_calibrated_parameters() -> Dict:
    """
    Return complete set of calibrated parameters for simulation.
    """
    return {
        'fema': FEMAParameters(),
        'discount_rates': DiscountRateParameters(),
        'climate': ClimateProjections(),
        'flood_frequency': FloodFrequencyParameters(),
        'depth_damage': USACEDepthDamage(),
        'property': PropertyParameters(),
        'brooklyn': BrooklynCaseStudyData(),
        'local_gov': LocalGovernmentParameters(),
        'equity_baseline': EquityBaselineData(),
    }


def get_all_case_studies() -> Dict:
    """
    Return all case study data for multi-region simulation.

    Returns dictionary with region names as keys and case study data as values.
    Total: 9 regions, ~34,500 households across diverse US flood-prone areas.
    """
    return {
        # NYC Metro Area (4 regions)
        'brooklyn_ny': BrooklynCaseStudyData(),
        'staten_island_ny': StatenIslandCaseStudyData(),
        'queens_ny': QueensCaseStudyData(),
        'lower_manhattan_ny': LowerManhattanCaseStudyData(),

        # Gulf Coast (2 regions)
        'houston_tx': HoustonCaseStudyData(),
        'new_orleans_la': NewOrleansCaseStudyData(),

        # Southeast (2 regions)
        'miami_dade_fl': MiamiDadeCaseStudyData(),
        'charleston_sc': CharlestonSCCaseStudyData(),

        # Mid-Atlantic (1 region)
        'norfolk_va': NorfolkVACaseStudyData(),
    }


def get_regional_summary() -> Dict:
    """
    Return summary statistics for all case study regions.
    """
    case_studies = get_all_case_studies()

    summary = {
        'total_regions': len(case_studies),
        'total_households': 0,
        'regions': {}
    }

    for name, data in case_studies.items():
        # Handle Manhattan differently (uses n_single_family_equivalent)
        if hasattr(data, 'n_single_family_equivalent'):
            n_homes = data.n_single_family_equivalent
        else:
            n_homes = data.n_single_family_homes

        summary['total_households'] += n_homes

        summary['regions'][name] = {
            'n_households': n_homes,
            'n_zip_codes': len(data.zip_codes),
            'house_value_mean': data.house_value_mean,
            'pct_low_income': data.pct_low_income,
            'pct_in_100yr_floodplain': data.pct_in_100yr_floodplain,
            'elevation_mean': data.elevation_mean,
        }

    return summary


def print_parameter_summary():
    """Print summary of key parameters with sources."""
    params = get_calibrated_parameters()

    print("=" * 70)
    print("CALIBRATED MODEL PARAMETERS WITH SOURCES")
    print("=" * 70)

    print("\n### FEMA HMGP Cost-Sharing ###")
    print(f"Standard Federal Share: {params['fema'].federal_share_standard:.0%}")
    print(f"Enhanced Federal Share: {params['fema'].federal_share_enhanced:.0%}")
    print("Source: FEMA.gov Cost Sharing Policy")

    print("\n### Discount Rates ###")
    print(f"Federal Social Rate: {params['discount_rates'].federal_social_discount_rate:.1%}")
    print(f"High-Income Household: {params['discount_rates'].household_high_income:.0%}")
    print(f"Low-Income Household: {params['discount_rates'].household_low_income:.0%}")
    print("Source: Warner & Pleeter (2001) AER, Hausman (1979)")

    print("\n### Sea Level Rise by 2100 ###")
    print(f"RCP 2.6 (Optimistic): {params['climate'].rcp26_2100[0]:.2f}m "
          f"[{params['climate'].rcp26_2100[1]:.2f}-{params['climate'].rcp26_2100[2]:.2f}m]")
    print(f"RCP 4.5 (Moderate): {params['climate'].rcp45_2100[0]:.2f}m "
          f"[{params['climate'].rcp45_2100[1]:.2f}-{params['climate'].rcp45_2100[2]:.2f}m]")
    print(f"RCP 8.5 (Pessimistic): {params['climate'].rcp85_2100[0]:.2f}m "
          f"[{params['climate'].rcp85_2100[1]:.2f}-{params['climate'].rcp85_2100[2]:.2f}m]")
    print("Source: IPCC SROCC (2019)")

    print("\n### Property Values (Brooklyn) ###")
    print(f"Median in Flood Zone: ${params['property'].brooklyn_median_flood_zone_2023:,.0f}")
    print(f"Median Outside Flood Zone: ${params['property'].brooklyn_median_non_flood_2023:,.0f}")
    print(f"Flood Zone Discount: ${params['property'].brooklyn_flood_discount:,.0f}")
    print("Source: PropertyShark (2023)")

    print("\n### Relocation Costs ###")
    print(f"Moving Cost (local): ${params['property'].local_move_avg:,.0f}")
    print(f"Moving Cost (long-distance): ${params['property'].long_distance_avg:,.0f}")
    print(f"Psychic Cost (median): ${params['property'].psychic_cost_median:,.0f}")
    print("Source: American Moving & Storage Association, Migration Economics Literature")

    print("\n" + "=" * 70)


def print_regional_summary():
    """Print summary of all case study regions."""
    summary = get_regional_summary()

    print("=" * 80)
    print("MULTI-REGION CASE STUDY SUMMARY")
    print("=" * 80)

    print(f"\nTotal Regions: {summary['total_regions']}")
    print(f"Total Households: {summary['total_households']:,}")

    print("\n" + "-" * 80)
    print(f"{'Region':<22} {'Homes':>8} {'ZIPs':>6} {'Avg Value':>12} "
          f"{'Low-Inc':>8} {'100yr FP':>9} {'Elev':>6}")
    print("-" * 80)

    for name, data in summary['regions'].items():
        region_display = name.replace('_', ' ').title()
        print(f"{region_display:<22} {data['n_households']:>8,} {data['n_zip_codes']:>6} "
              f"${data['house_value_mean']:>10,.0f} {data['pct_low_income']:>7.0%} "
              f"{data['pct_in_100yr_floodplain']:>8.0%} {data['elevation_mean']:>5.1f}m")

    print("-" * 80)

    # Regional groupings
    print("\n### Regional Breakdown ###")
    print("\nNYC Metro Area (4 regions):")
    print("  Brooklyn, Staten Island, Queens, Lower Manhattan")
    print("  Key event: Hurricane Sandy (2012)")

    print("\nGulf Coast (2 regions):")
    print("  Houston TX, New Orleans LA")
    print("  Key events: Hurricane Harvey (2017), Hurricane Katrina (2005)")

    print("\nSoutheast Atlantic (2 regions):")
    print("  Miami-Dade FL, Charleston SC")
    print("  Key issues: Chronic sea level rise, insurance crisis")

    print("\nMid-Atlantic (1 region):")
    print("  Norfolk VA")
    print("  Key issues: Military infrastructure, land subsidence")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    print_parameter_summary()
    print("\n\n")
    print_regional_summary()
