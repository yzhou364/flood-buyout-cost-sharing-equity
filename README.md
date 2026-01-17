# Equity Implications of Federal-Local Cost-Sharing in Flood Buyouts: A Stochastic Game-Theoretic Analysis with Heterogeneous Homeowners

## Overview

This repository contains the research materials for a theoretical study on how federal-local cost-sharing arrangements in flood buyout programs affect both efficiency and equity outcomes. The study develops a novel **three-level stochastic Stackelberg game** model that explicitly captures the strategic interactions between:

1. **Federal Government** (Leader): Sets cost-sharing ratios and subsidy caps
2. **Local Governments** (Intermediate Followers): Decide program participation and subsidy levels
3. **Heterogeneous Homeowners** (Ultimate Followers): Make relocation timing decisions

## Key Research Question

> How do federal cost-sharing ratios influence local governments' buyout decisions, and what are the resulting equity implications for different income groups under uncertain future flood risks?

## Building Upon Prior Work

This research extends the foundational game-theoretic framework from:

- **Bier, V. M., Zhou, Y., & Du, H. (2019)**. *Game-theoretic modeling of pre-disaster relocation*. The Engineering Economist, 65(2), 89-113.
- **Zhou, Y. (2022)**. *Pre-disaster relocation and agent-based model for flood disaster*. Doctoral dissertation, University of Wisconsin-Madison.

## Repository Structure

```
.
├── paper/
│   └── main.tex              # Full LaTeX manuscript
├── code/
│   └── model.py              # Python implementation of the model
├── papers/
│   ├── proposal.md           # Original research proposal
│   └── Game-theoretic.pdf    # Bier et al. (2019) paper
└── README.md
```

## Mathematical Model Highlights

### Three-Level Game Structure

**Stage 1 (Federal):**
```
min_{α, S̄} E_ω[Σ_j (α · S_j* · N_j^rel + C_j^Fed)]
s.t.  Budget constraint
      Equity constraint: RRG ≥ θ
```

**Stage 2 (Local):**
```
min_{I_j, S_j} (1-α)S_j·N_j^rel + E[C_j^loc] + λ_j·ΔTaxBase
s.t.  S_j ≤ S̄
```

**Stage 3 (Homeowner):**
```
min_{k_h} (M_h - S_j)/(1+r_h)^k + Σ_{t<k} E[D_{h,t}]/(1+r_h)^t
```

### Key Theoretical Results

1. **Theorem (Homeowner Equilibrium)**: Higher discount rates (typical of low-income households) require larger subsidies to induce the same relocation timing.

2. **Theorem (Local Government Equilibrium)**: The participation threshold α_j^crit is higher for communities with stronger tax base preservation incentives.

3. **Proposition (Equity Impact)**: Higher federal cost-share ratios improve the Relocation Ratio Gap (RRG), benefiting low-income communities.

### Equity Metrics

- **Relocation Ratio Gap (RRG)**: (N_low^rel/N_low^total) / (N_high^rel/N_high^total)
- **Timing Gap**: Average years low-income households relocate later
- **Subsidy Gini Coefficient**: Inequality in subsidy distribution
- **Expected Damage Ratio**: Relative flood damage burden by income group

## Running the Simulation

```python
from code.model import run_simulation

# Run full simulation
results = run_simulation()

# Access results
print(f"Optimal alpha: {results['optimal_policy']['alpha']}")
print(f"Equity ratio: {results['optimal_policy']['equity_ratio']}")
```

## Policy Implications

The analysis yields several actionable policy recommendations:

1. **Equity-Weighted Cost Sharing**: Set α_j = ᾱ + γ·(MHI_nat - MHI_j) to provide higher federal shares to lower-income communities

2. **Income-Tiered Subsidies**: Offer S_h = S_base + ΔS for low-income households, where ΔS compensates for the discount rate gap

3. **Minimum Service Requirements**: Mandate that participating jurisdictions achieve minimum relocation rates for low-income households

## Target Journals

- Natural Hazards
- International Journal of Disaster Risk Reduction
- Climate Risk Management
- Risk Analysis
- Journal of Flood Risk Management

## Key References

```bibtex
@article{bier2019game,
  title={Game-theoretic modeling of pre-disaster relocation},
  author={Bier, Vicki M and Zhou, Yuqun and Du, Hongru},
  journal={The Engineering Economist},
  volume={65},
  number={2},
  pages={89--113},
  year={2019}
}

@phdthesis{zhou2022dissertation,
  title={Pre-disaster relocation and agent-based model for flood disaster},
  author={Zhou, Yuqun},
  year={2022},
  school={University of Wisconsin-Madison}
}

@article{elliott2021racial,
  title={Racial inequities in the federal buyout of flood-prone homes},
  author={Elliott, James R and Brown, Phylicia Lee and Loughran, Kevin},
  journal={Socius},
  volume={6},
  year={2021}
}
```

## License

This research is intended for academic publication. Please cite appropriately if using any materials from this repository.

## Contact

[Your Name]
[Your Institution]
[Your Email]
