"""
Sensitivity Analysis for Federal-Local Cost-Sharing Model
==========================================================

This module performs comprehensive sensitivity analysis on:
1. Maximum subsidy levels
2. Discount rate heterogeneity
3. Flood risk parameters
4. Climate scenario probabilities

Author: [Your Name]
Date: January 2026
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
import time
import logging

from model import (
    ClimateScenario, Household, LocalGovernment, FederalGovernment,
    FloodRiskModel, HomeownerModel, LocalGovernmentModel,
    FederalOptimizer, EquityAnalyzer
)
from real_parameters import get_calibrated_parameters, get_all_case_studies
from simulation_with_real_data import (
    create_ipcc_scenarios, create_calibrated_flood_model,
    create_regional_population, setup_logging
)

# Setup logging
logger = setup_logging(log_to_file=True)


def run_subsidy_sensitivity(
    jurisdictions: List[LocalGovernment],
    scenarios: List[ClimateScenario],
    subsidy_levels: List[float] = None,
    alpha_values: List[float] = None
) -> pd.DataFrame:
    """
    Analyze sensitivity to maximum subsidy cap.

    Args:
        jurisdictions: List of local governments
        scenarios: Climate scenarios
        subsidy_levels: List of max subsidy values to test
        alpha_values: List of federal cost-share ratios

    Returns:
        DataFrame with results for each subsidy/alpha combination
    """
    if subsidy_levels is None:
        subsidy_levels = [150000, 200000, 250000, 300000, 350000, 400000, 500000]
    if alpha_values is None:
        alpha_values = [0.75, 0.85, 0.90, 1.00]

    logger.info("=" * 60)
    logger.info("SENSITIVITY ANALYSIS: Maximum Subsidy Cap")
    logger.info("=" * 60)

    # Initialize models
    flood_model = create_calibrated_flood_model()
    homeowner_model = HomeownerModel(flood_model, scenarios, planning_horizon=80)
    local_gov_model = LocalGovernmentModel(homeowner_model, scenarios)

    params = get_calibrated_parameters()
    federal_gov = FederalGovernment(
        discount_rate=params['discount_rates'].federal_social_discount_rate,
        budget=2.5e9,
        equity_threshold=0.70
    )

    federal_optimizer = FederalOptimizer(local_gov_model, federal_gov, jurisdictions)

    results = []
    total_runs = len(subsidy_levels) * len(alpha_values)
    run_count = 0

    for max_subsidy in subsidy_levels:
        for alpha in alpha_values:
            run_count += 1
            start = time.time()

            outcomes = federal_optimizer.evaluate_policy(alpha, max_subsidy)
            elapsed = time.time() - start

            results.append({
                'max_subsidy': max_subsidy,
                'alpha': alpha,
                'total_relocations': outcomes['total_relocations'],
                'low_income_relocations': outcomes['low_income_relocations'],
                'high_income_relocations': outcomes['high_income_relocations'],
                'equity_ratio': outcomes['equity_ratio'],
                'total_federal_cost': outcomes['total_federal_cost'],
                'free_riders': outcomes['free_riders'],
                'participating_jurisdictions': outcomes['participating_jurisdictions']
            })

            logger.info(f"  [{run_count}/{total_runs}] Subsidy=${max_subsidy:,}, alpha={alpha:.0%}: "
                       f"RRG={outcomes['equity_ratio']:.3f}, Relocations={outcomes['total_relocations']} ({elapsed:.2f}s)")

    return pd.DataFrame(results)


def run_discount_rate_sensitivity(
    base_jurisdictions: List[LocalGovernment],
    scenarios: List[ClimateScenario],
    discount_rate_scenarios: Dict[str, Tuple[float, float]] = None
) -> pd.DataFrame:
    """
    Analyze sensitivity to household discount rate assumptions.

    Args:
        base_jurisdictions: Base population (will be modified)
        scenarios: Climate scenarios
        discount_rate_scenarios: Dict of scenario name -> (low_income_rate, high_income_rate)

    Returns:
        DataFrame with results for each discount rate scenario
    """
    if discount_rate_scenarios is None:
        discount_rate_scenarios = {
            'Base Case (Bier 2019)': (0.20, 0.10),
            'Low Heterogeneity': (0.15, 0.12),
            'High Heterogeneity': (0.25, 0.08),
            'Warner & Pleeter (2001)': (0.18, 0.10),
            'Extreme Credit Constraint': (0.30, 0.10),
        }

    logger.info("=" * 60)
    logger.info("SENSITIVITY ANALYSIS: Discount Rate Heterogeneity")
    logger.info("=" * 60)

    results = []
    alpha = 0.85  # Use optimal alpha from main analysis
    max_subsidy = 250000

    for scenario_name, (low_rate, high_rate) in discount_rate_scenarios.items():
        logger.info(f"  Testing: {scenario_name} (low={low_rate:.0%}, high={high_rate:.0%})")

        # Modify discount rates in households
        modified_jurisdictions = []
        for j in base_jurisdictions:
            new_j = LocalGovernment(
                id=j.id,
                discount_rate=j.discount_rate,
                tax_rate=j.tax_rate,
                tax_base_weight=j.tax_base_weight,
                admin_cost=j.admin_cost
            )
            new_households = []
            for h in j.households:
                # Set discount rate based on income group
                if h.income_group == 'low':
                    new_rate = np.random.uniform(low_rate - 0.02, low_rate + 0.02)
                else:
                    new_rate = np.random.uniform(high_rate - 0.02, high_rate + 0.02)

                new_h = Household(
                    id=h.id,
                    jurisdiction=h.jurisdiction,
                    house_value=h.house_value,
                    structure_value=h.structure_value,
                    elevation=h.elevation,
                    discount_rate=new_rate,
                    income_group=h.income_group,
                    moving_cost=h.moving_cost,
                    psychic_cost=h.psychic_cost
                )
                new_households.append(new_h)
            new_j.households = new_households
            modified_jurisdictions.append(new_j)

        # Run simulation with modified population
        flood_model = create_calibrated_flood_model()
        homeowner_model = HomeownerModel(flood_model, scenarios, planning_horizon=80)
        local_gov_model = LocalGovernmentModel(homeowner_model, scenarios)

        params = get_calibrated_parameters()
        federal_gov = FederalGovernment(
            discount_rate=params['discount_rates'].federal_social_discount_rate,
            budget=2.5e9,
            equity_threshold=0.70
        )

        federal_optimizer = FederalOptimizer(local_gov_model, federal_gov, modified_jurisdictions)
        outcomes = federal_optimizer.evaluate_policy(alpha, max_subsidy)

        results.append({
            'scenario': scenario_name,
            'low_income_discount_rate': low_rate,
            'high_income_discount_rate': high_rate,
            'discount_rate_gap': low_rate - high_rate,
            'total_relocations': outcomes['total_relocations'],
            'low_income_relocations': outcomes['low_income_relocations'],
            'high_income_relocations': outcomes['high_income_relocations'],
            'equity_ratio': outcomes['equity_ratio'],
            'total_federal_cost': outcomes['total_federal_cost'],
        })

        logger.info(f"    RRG={outcomes['equity_ratio']:.3f}, Relocations={outcomes['total_relocations']}")

    return pd.DataFrame(results)


def run_climate_sensitivity(
    jurisdictions: List[LocalGovernment],
    climate_scenarios_list: Dict[str, List[ClimateScenario]] = None
) -> pd.DataFrame:
    """
    Analyze sensitivity to climate scenario assumptions.

    Args:
        jurisdictions: List of local governments
        climate_scenarios_list: Dict of scenario set name -> list of ClimateScenario

    Returns:
        DataFrame with results for each climate scenario set
    """
    if climate_scenarios_list is None:
        # Define different climate scenario probability distributions
        climate_scenarios_list = {
            'IPCC Baseline': [
                ClimateScenario("RCP2.6", 0.15, 0.43),
                ClimateScenario("RCP4.5", 0.50, 0.53),
                ClimateScenario("RCP8.5", 0.35, 0.84),
            ],
            'Optimistic (Paris Success)': [
                ClimateScenario("RCP2.6", 0.50, 0.43),
                ClimateScenario("RCP4.5", 0.35, 0.53),
                ClimateScenario("RCP8.5", 0.15, 0.84),
            ],
            'Pessimistic (BAU)': [
                ClimateScenario("RCP2.6", 0.10, 0.43),
                ClimateScenario("RCP4.5", 0.30, 0.53),
                ClimateScenario("RCP8.5", 0.60, 0.84),
            ],
            'High SLR (NOAA High)': [
                ClimateScenario("RCP2.6", 0.15, 0.60),
                ClimateScenario("RCP4.5", 0.50, 0.80),
                ClimateScenario("RCP8.5", 0.35, 1.20),
            ],
        }

    logger.info("=" * 60)
    logger.info("SENSITIVITY ANALYSIS: Climate Scenario Assumptions")
    logger.info("=" * 60)

    results = []
    alpha = 0.85
    max_subsidy = 250000

    for scenario_name, scenarios in climate_scenarios_list.items():
        logger.info(f"  Testing: {scenario_name}")

        flood_model = create_calibrated_flood_model()
        homeowner_model = HomeownerModel(flood_model, scenarios, planning_horizon=80)
        local_gov_model = LocalGovernmentModel(homeowner_model, scenarios)

        params = get_calibrated_parameters()
        federal_gov = FederalGovernment(
            discount_rate=params['discount_rates'].federal_social_discount_rate,
            budget=2.5e9,
            equity_threshold=0.70
        )

        federal_optimizer = FederalOptimizer(local_gov_model, federal_gov, jurisdictions)
        outcomes = federal_optimizer.evaluate_policy(alpha, max_subsidy)

        # Calculate expected SLR
        expected_slr = sum(s.probability * s.slr_2100 for s in scenarios)

        results.append({
            'scenario': scenario_name,
            'expected_slr_2100': expected_slr,
            'prob_rcp85': next((s.probability for s in scenarios if 'RCP8.5' in s.name), 0),
            'total_relocations': outcomes['total_relocations'],
            'low_income_relocations': outcomes['low_income_relocations'],
            'equity_ratio': outcomes['equity_ratio'],
            'total_federal_cost': outcomes['total_federal_cost'],
        })

        logger.info(f"    Expected SLR={expected_slr:.2f}m, RRG={outcomes['equity_ratio']:.3f}")

    return pd.DataFrame(results)


def validate_against_real_data() -> pd.DataFrame:
    """
    Compare model predictions with actual buyout program data.

    Sources:
    - FEMA HMGP buyout data
    - Harris County (Houston) buyout program
    - Staten Island buyout program
    - New Jersey Blue Acres program
    """
    logger.info("=" * 60)
    logger.info("MODEL VALIDATION: Comparison with Real Buyout Data")
    logger.info("=" * 60)

    # Real buyout program data
    real_data = {
        'Staten Island NY (Sandy)': {
            'year': 2013,
            'homes_eligible': 500,
            'homes_bought_out': 326,
            'participation_rate': 0.65,
            'avg_buyout_price': 310000,
            'low_income_pct': 0.45,
            'federal_share': 0.75,
        },
        'Harris County TX (Harvey)': {
            'year': 2017,
            'homes_eligible': 5000,
            'homes_bought_out': 3500,
            'participation_rate': 0.70,
            'avg_buyout_price': 195000,
            'low_income_pct': 0.55,
            'federal_share': 0.75,
        },
        'New Jersey Blue Acres': {
            'year': 2013,
            'homes_eligible': 1300,
            'homes_bought_out': 700,
            'participation_rate': 0.54,
            'avg_buyout_price': 225000,
            'low_income_pct': 0.40,
            'federal_share': 0.75,
        },
        'Charlotte-Mecklenburg NC': {
            'year': 1999,
            'homes_eligible': 450,
            'homes_bought_out': 400,
            'participation_rate': 0.89,
            'avg_buyout_price': 85000,
            'low_income_pct': 0.60,
            'federal_share': 0.75,
        },
    }

    # Model predictions at alpha=0.75
    model_predictions = {
        'Staten Island NY (Sandy)': {
            'predicted_participation': 0.026,  # From multi-region results
            'predicted_equity_ratio': 0.26,
        },
        'Harris County TX (Harvey)': {
            'predicted_participation': 0.026,
            'predicted_equity_ratio': 0.26,
        },
        'New Jersey Blue Acres': {
            'predicted_participation': 0.026,
            'predicted_equity_ratio': 0.26,
        },
        'Charlotte-Mecklenburg NC': {
            'predicted_participation': 0.026,
            'predicted_equity_ratio': 0.26,
        },
    }

    validation_results = []
    for program, data in real_data.items():
        pred = model_predictions.get(program, {})
        validation_results.append({
            'program': program,
            'year': data['year'],
            'real_participation_rate': data['participation_rate'],
            'model_participation_rate': pred.get('predicted_participation', np.nan),
            'participation_error': abs(data['participation_rate'] - pred.get('predicted_participation', 0)),
            'real_avg_price': data['avg_buyout_price'],
            'real_low_income_pct': data['low_income_pct'],
            'federal_share': data['federal_share'],
        })

    df = pd.DataFrame(validation_results)

    logger.info("\nValidation Summary:")
    logger.info("-" * 60)
    for _, row in df.iterrows():
        logger.info(f"  {row['program']}: Real={row['real_participation_rate']:.0%}, "
                   f"Model={row['model_participation_rate']:.1%}")

    return df


def run_full_sensitivity_analysis():
    """
    Run complete sensitivity analysis suite.
    """
    overall_start = time.time()
    logger.info("=" * 70)
    logger.info("COMPREHENSIVE SENSITIVITY ANALYSIS")
    logger.info("=" * 70)

    # Create base population (use subset for faster analysis)
    logger.info("\nCreating base population...")
    case_studies = get_all_case_studies()
    scenarios = create_ipcc_scenarios('nyc')

    # Use 3 representative regions for sensitivity
    selected_regions = ['houston_tx', 'new_orleans_la', 'norfolk_va']

    all_jurisdictions = []
    jurisdiction_id = 0
    household_id = 0

    for region_name in selected_regions:
        region_data = case_studies[region_name]
        jurisdictions, jurisdiction_id, household_id = create_regional_population(
            region_name, region_data,
            jurisdiction_start_id=jurisdiction_id,
            household_start_id=household_id,
            seed=42
        )
        all_jurisdictions.extend(jurisdictions)

    total_households = sum(len(j.households) for j in all_jurisdictions)
    logger.info(f"Created {total_households:,} households across {len(all_jurisdictions)} jurisdictions")

    # Output directory
    output_dir = Path(__file__).parent / 'output' / 'sensitivity'
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Subsidy sensitivity
    logger.info("\n" + "=" * 60)
    logger.info("ANALYSIS 1: Maximum Subsidy Sensitivity")
    subsidy_results = run_subsidy_sensitivity(all_jurisdictions, scenarios)
    subsidy_results.to_csv(output_dir / 'subsidy_sensitivity.csv', index=False)
    logger.info(f"Saved to {output_dir / 'subsidy_sensitivity.csv'}")

    # 2. Discount rate sensitivity
    logger.info("\n" + "=" * 60)
    logger.info("ANALYSIS 2: Discount Rate Sensitivity")
    discount_results = run_discount_rate_sensitivity(all_jurisdictions, scenarios)
    discount_results.to_csv(output_dir / 'discount_rate_sensitivity.csv', index=False)
    logger.info(f"Saved to {output_dir / 'discount_rate_sensitivity.csv'}")

    # 3. Climate sensitivity
    logger.info("\n" + "=" * 60)
    logger.info("ANALYSIS 3: Climate Scenario Sensitivity")
    climate_results = run_climate_sensitivity(all_jurisdictions)
    climate_results.to_csv(output_dir / 'climate_sensitivity.csv', index=False)
    logger.info(f"Saved to {output_dir / 'climate_sensitivity.csv'}")

    # 4. Validation
    logger.info("\n" + "=" * 60)
    logger.info("ANALYSIS 4: Real Data Validation")
    validation_results = validate_against_real_data()
    validation_results.to_csv(output_dir / 'validation_results.csv', index=False)
    logger.info(f"Saved to {output_dir / 'validation_results.csv'}")

    total_time = time.time() - overall_start
    logger.info("\n" + "=" * 70)
    logger.info("SENSITIVITY ANALYSIS COMPLETE")
    logger.info(f"Total time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    logger.info(f"Results saved to: {output_dir}")
    logger.info("=" * 70)

    return {
        'subsidy': subsidy_results,
        'discount_rate': discount_results,
        'climate': climate_results,
        'validation': validation_results,
    }


if __name__ == "__main__":
    results = run_full_sensitivity_analysis()

    print("\n=== SENSITIVITY ANALYSIS SUMMARY ===\n")

    print("1. Subsidy Sensitivity (alpha=85%, varying max subsidy):")
    subsidy_85 = results['subsidy'][results['subsidy']['alpha'] == 0.85]
    print(subsidy_85[['max_subsidy', 'total_relocations', 'equity_ratio']].to_string(index=False))

    print("\n2. Discount Rate Sensitivity:")
    print(results['discount_rate'][['scenario', 'discount_rate_gap', 'equity_ratio']].to_string(index=False))

    print("\n3. Climate Scenario Sensitivity:")
    print(results['climate'][['scenario', 'expected_slr_2100', 'equity_ratio']].to_string(index=False))
