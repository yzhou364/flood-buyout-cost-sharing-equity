# Research Proposal

# Equity Implications of Federal-Local Cost-Sharing in Flood Buyouts: A Stochastic Game-Theoretic Analysis with Heterogeneous Homeowners

---

**Author:** [Your Name]  
**Affiliation:** [Your Institution]  
**Date:** January 2026  
**Status:** Research Proposal for Independent Publication

---

## Executive Summary

This research proposes a novel stochastic game-theoretic framework to analyze how federal-local cost-sharing arrangements in flood buyout programs affect both efficiency and equity outcomes. By modeling the strategic interactions between federal government, local governments, and heterogeneous homeowners under climate uncertainty, this study addresses a critical gap in the managed retreat literature. The research builds upon prior work on agent-based modeling of flood relocation decisions and extends it to incorporate multi-level governmental decision-making and stochastic climate scenarios.

**Key Research Question:** How do federal cost-sharing ratios influence local governments' buyout decisions, and what are the resulting equity implications for low-income versus high-income homeowners under uncertain future flood risks?

---

## Table of Contents

1. [Introduction and Motivation](#1-introduction-and-motivation)
2. [Literature Review and Research Gap](#2-literature-review-and-research-gap)
3. [Research Questions and Objectives](#3-research-questions-and-objectives)
4. [Theoretical Framework](#4-theoretical-framework)
5. [Methodology](#5-methodology)
6. [Data Requirements](#6-data-requirements)
7. [Expected Contributions](#7-expected-contributions)
8. [Timeline and Milestones](#8-timeline-and-milestones)
9. [Target Journals](#9-target-journals)
10. [References](#10-references)

---

## 1. Introduction and Motivation

### 1.1 Background: The Buyout Policy Landscape

Managed retreat through property buyouts has emerged as an increasingly important climate adaptation strategy in the United States. The Federal Emergency Management Agency (FEMA) administers the primary buyout programs, including the Hazard Mitigation Grant Program (HMGP) and Building Resilient Infrastructure and Communities (BRIC) program. These programs typically operate on a **cost-sharing basis**, with the federal government covering 75% of costs and state/local governments responsible for the remaining 25%.

However, this seemingly straightforward arrangement masks complex strategic interactions:

```
Current Policy Structure:
┌─────────────────────────────────────────────────────────────┐
│  FEDERAL (FEMA)          STATE              LOCAL          │
│  ───────────────         ─────              ─────          │
│  • Sets matching ratio   • Administers      • Applies for  │
│    (typically 75%)         funds              grants       │
│  • Approves projects     • Provides some    • Implements   │
│  • Bears majority cost     matching funds     buyouts      │
│                                             • Loses tax    │
│                                               base         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  HOMEOWNERS (Heterogeneous)                                 │
│  ─────────────────────────                                  │
│  • Decide whether to accept buyout                          │
│  • Vary by income, discount rate, flood exposure            │
│  • Face uncertain future flood risks                        │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 The Problem: Equity Concerns in Buyout Implementation

Recent empirical research has documented significant equity concerns in buyout programs:

- **Elliott et al. (2021)** found that buyout funding is disproportionately allocated to wealthier, white communities
- **Kousky et al. (2021)** documented that high-income homeowners receive systematically larger buyouts
- **Flavelle (2019)** reported that wealthier counties receive more federal assistance for flood adaptation
- **Marino (2018)** noted that buyout policies have disadvantaged tribal communities

These disparities may arise, in part, from the **incentive structure embedded in cost-sharing arrangements**. Local governments facing a 25% cost share may be more likely to pursue buyouts in affluent areas where:
1. Property values (and thus buyout costs) can be partially recovered through future land use
2. Political constituents have more influence
3. Administrative capacity to apply for federal grants is higher

### 1.3 The Gap: Missing Multi-Level Strategic Analysis

Existing models of flood relocation (including our prior work, Bier et al. 2018, 2022; Zhou 2022) treat government as a **single unified decision-maker**. This simplification ignores:

1. **Divergent objectives** between federal and local governments
2. **Strategic responses** of local governments to federal policy parameters
3. **Climate uncertainty** and its differential impact on government decision-making
4. **Feedback effects** between governmental decisions and household-level outcomes

This research addresses these gaps by developing a **stochastic Stackelberg game** that explicitly models federal-local interactions under climate uncertainty.

---

## 2. Literature Review and Research Gap

### 2.1 Related Literature Streams

This research draws from and contributes to four literature streams:

#### Stream 1: Managed Retreat and Flood Buyouts

| Key Studies | Contribution | Limitation |
|-------------|--------------|------------|
| Freudenberg et al. (2016) | Comprehensive review of buyout challenges | No formal modeling |
| Mach et al. (2019, Science) | Framework for managed retreat governance | Qualitative, no strategic analysis |
| Siders et al. (2019) | Social equity in managed retreat | Conceptual, not quantitative |
| BenDor et al. (2020) | Empirical analysis of FEMA buyouts | Descriptive, no game-theoretic framework |

#### Stream 2: Game Theory in Disaster Management

| Key Studies | Contribution | Limitation |
|-------------|--------------|------------|
| Guan & Zhuang (2015) | Public-private disaster preparedness games | Not specific to relocation |
| Hausken & Zhuang (2016) | Government-firm safety investment games | No multi-level government |
| Jeong et al. (2018) | Cooperative game for flood adaptation | Stakeholder game, not federal-local |

#### Stream 3: Fiscal Federalism and Environmental Policy

| Key Studies | Contribution | Limitation |
|-------------|--------------|------------|
| Oates (1999) | Environmental federalism theory | Not climate adaptation specific |
| Sigman (2005) | Strategic behavior in environmental regulation | Water quality, not flood risk |
| Slavikova (2018) | Crowding-out in flood protection spending | Empirical, no formal game model |

#### Stream 4: Stochastic Programming in Climate Adaptation

| Key Studies | Contribution | Limitation |
|-------------|--------------|------------|
| Giuliani & Castelletti (2016) | Robustness in climate decisions | Water resources, not relocation |
| Hecht & Kirshen (2019) | Deep uncertainty in floodplain management | Single decision-maker |
| Hinkel et al. (2019) | Sea-level rise decision analysis | No game-theoretic interaction |

### 2.2 Identified Research Gap

```
                    Existing Research Coverage
                    
                         Game Theory
                              │
              ┌───────────────┼───────────────┐
              │               │               │
        Public-Private    Stakeholder    Federal-Local
        Partnerships      Coordination   Cost-Sharing
        (Guan & Zhuang)   (Jeong et al.)     │
                                             │
                                    ┌────────┴────────┐
                                    │   THIS STUDY    │
                                    │                 │
                                    │ • Multi-level   │
                                    │   government    │
                                    │ • Heterogeneous │
                                    │   homeowners    │
                                    │ • Stochastic    │
                                    │   climate       │
                                    │ • Equity focus  │
                                    └─────────────────┘
```

**No existing study combines:**
1. Multi-level government strategic interaction
2. Heterogeneous homeowner decision-making
3. Stochastic climate uncertainty
4. Explicit equity analysis

in the context of flood buyouts and managed retreat.

---

## 3. Research Questions and Objectives

### 3.1 Central Research Question

> **How do federal cost-sharing ratios influence local governments' buyout decisions, and what are the resulting equity implications for different income groups under uncertain future flood risks?**

### 3.2 Specific Research Questions

**RQ1 (Efficiency):** What is the equilibrium buyout subsidy level under different federal cost-sharing ratios, and how does it compare to the socially optimal level?

**RQ2 (Strategic Behavior):** Does a high federal cost-sharing ratio induce "free-riding" behavior by local governments (e.g., waiting for federal funds rather than proactive investment)?

**RQ3 (Equity):** How do different cost-sharing arrangements affect the distribution of buyout benefits across income groups? Specifically:
- Do low-income homeowners systematically receive fewer/later buyout offers?
- Does the current 75/25 federal-local split exacerbate or mitigate income-based disparities?

**RQ4 (Uncertainty):** How does climate uncertainty affect the optimal cost-sharing ratio, and does accounting for uncertainty change the equity implications?

**RQ5 (Policy Design):** Can alternative cost-sharing mechanisms (e.g., equity-weighted matching, sliding scale based on community income) improve both efficiency and equity?

### 3.3 Research Objectives

1. **Develop** a two-stage stochastic Stackelberg game model of federal-local-homeowner interactions
2. **Calibrate** the model using real-world data from Brooklyn, NY (building on prior dissertation work)
3. **Analyze** equilibrium outcomes under various cost-sharing scenarios
4. **Quantify** equity implications using income-stratified metrics
5. **Identify** policy recommendations for improving buyout program design

---

## 4. Theoretical Framework

### 4.1 Game Structure Overview

We model the buyout decision process as a **two-stage stochastic Stackelberg game**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 1: FEDERAL DECISION                    │
│                    (Leader, moves first)                        │
├─────────────────────────────────────────────────────────────────┤
│  Decision Variables:                                            │
│  • α ∈ [0,1]: Federal cost-sharing ratio                       │
│  • S̄: Maximum allowable subsidy per household                  │
│                                                                 │
│  Objective: Minimize expected total cost (subsidies + disaster  │
│             damages) across all climate scenarios               │
│                                                                 │
│  Constraints: Budget constraints, equity requirements           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 2: LOCAL + HOMEOWNER                   │
│                    (Followers, respond to federal policy)       │
├─────────────────────────────────────────────────────────────────┤
│  LOCAL GOVERNMENT:                                              │
│  • Observes federal policy (α, S̄)                              │
│  • Decides whether to apply for buyout program                  │
│  • Sets local subsidy level S ≤ S̄                              │
│  • Trades off: (1-α)·cost vs. tax base loss vs. disaster costs │
│                                                                 │
│  HOMEOWNERS (via Agent-Based Model):                            │
│  • Heterogeneous by income, discount rate, location             │
│  • Decide whether/when to accept buyout offer                   │
│  • Face uncertain future flood risks                            │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Notation

| Symbol | Description | Unit |
|--------|-------------|------|
| **Indices** | | |
| $t$ | Time period (year) | - |
| $j$ | Local jurisdiction (zip code or municipality) | - |
| $h$ | Individual household | - |
| $\omega$ | Climate scenario | - |
| **Federal Decision Variables** | | |
| $\alpha$ | Federal cost-sharing ratio | [0,1] |
| $\bar{S}$ | Maximum subsidy cap | $ |
| **Local Decision Variables** | | |
| $I_j \in \{0,1\}$ | Binary: whether jurisdiction $j$ applies for buyout program | - |
| $S_j$ | Subsidy level offered in jurisdiction $j$ | $ |
| **Homeowner Decision Variables** | | |
| $k_h^*$ | Year in which household $h$ relocates | year |
| **Parameters** | | |
| $r_F$ | Federal discount rate | % |
| $r_L$ | Local government discount rate | % |
| $r_R^{high}, r_R^{low}$ | Homeowner discount rates (by income) | % |
| $M_h$ | Relocation cost for household $h$ | $ |
| $D_{h,t,\omega}$ | Flood damage to household $h$ in year $t$, scenario $\omega$ | $ |
| $P(\omega)$ | Probability of climate scenario $\omega$ | [0,1] |
| $\lambda_j$ | Local government's weight on tax base preservation | - |
| $\tau$ | Property tax rate | % |

### 4.3 Mathematical Formulation

#### 4.3.1 Federal Government's Problem (Stage 1)

The federal government solves a **stochastic optimization problem**:

$$\min_{\alpha, \bar{S}} \quad \mathbb{E}_{\omega} \left[ \sum_{j} \left( \alpha \cdot S_j^*(\alpha, \bar{S}, \omega) \cdot N_j^{relocate}(\alpha, \bar{S}, \omega) + C_j^{Fed}(\alpha, \bar{S}, \omega) \right) \right]$$

Subject to:
$$\sum_j \alpha \cdot S_j^* \cdot N_j^{relocate} \leq B^{Fed} \quad \text{(Budget constraint)}$$

$$\frac{N_{low-income}^{relocate}}{N_{low-income}^{total}} \geq \theta \cdot \frac{N_{high-income}^{relocate}}{N_{high-income}^{total}} \quad \text{(Equity constraint)}$$

$$\alpha \in [\underline{\alpha}, \bar{\alpha}] \quad \text{(Policy feasibility)}$$

Where:
- $S_j^*(\alpha, \bar{S}, \omega)$ is the local government's equilibrium subsidy (from Stage 2)
- $N_j^{relocate}$ is the number of households accepting buyouts
- $C_j^{Fed}$ is federal disaster relief costs for non-relocated households
- $B^{Fed}$ is the federal budget
- $\theta \in [0,1]$ is the equity parameter (higher = stricter equity requirement)

#### 4.3.2 Local Government's Problem (Stage 2a)

Given federal policy $(\alpha, \bar{S})$ and climate scenario $\omega$, each local government solves:

$$\min_{S_j, I_j} \quad (1-\alpha) \cdot S_j \cdot N_j^{relocate} \cdot I_j + C_j^{Local}(\omega) - \lambda_j \cdot \Delta TaxBase_j$$

Subject to:
$$S_j \leq \bar{S}$$
$$I_j \in \{0, 1\}$$

Where:
- $(1-\alpha) \cdot S_j$ is the local cost share per buyout
- $C_j^{Local}(\omega)$ is local disaster-related costs (infrastructure repair, emergency services)
- $\Delta TaxBase_j = \tau \cdot \sum_{h \in relocated} V_h$ is the present value of lost property tax revenue
- $\lambda_j$ captures how much the local government prioritizes tax base preservation

**Key Trade-off for Local Government:**
```
         Apply for Buyout (I_j = 1)              Don't Apply (I_j = 0)
         ─────────────────────────               ───────────────────────
Costs:   (1-α)·S·N relocations                  Expected disaster costs
         + Administrative burden                 
                                                 
Benefits: Reduced disaster exposure              Preserve tax base
          Federal funds (α portion)              Avoid administrative costs
```

#### 4.3.3 Homeowner's Problem (Stage 2b)

Building on prior work (Bier et al. 2018; Zhou 2022), each household decides when to relocate by comparing:

$$\min_{k_h} \quad I_{k_h}(M_h - S_j^*) + (1 - I_{k_h}) \sum_{t=k_h}^{T} \frac{\mathbb{E}_\omega[D_{h,t,\omega}]}{(1+r_R^h)^{t-k_h}}$$

Where:
- $k_h$ is the relocation year
- $I_{k_h} = 1$ if household relocates in year $k_h$
- $M_h$ is the total relocation cost (house value + moving costs)
- $r_R^h$ is the household's discount rate (varies by income)

**Income-Based Heterogeneity:**
| Income Group | Discount Rate | Relocation Cost | Typical Behavior |
|--------------|---------------|-----------------|------------------|
| High-income | $r_R^{high}$ = 12% | Higher (larger homes) | May relocate without subsidy |
| Low-income | $r_R^{low}$ = 18% | Lower (smaller homes) | Needs substantial subsidy |

### 4.4 Stochastic Climate Scenarios

We model climate uncertainty through discrete scenarios based on Representative Concentration Pathways (RCPs):

| Scenario $\omega$ | Description | Sea-Level Rise by 2100 | Probability $P(\omega)$ |
|-------------------|-------------|------------------------|-------------------------|
| $\omega_1$ | Optimistic (RCP 2.6) | ~0.4m | 0.2 |
| $\omega_2$ | Moderate (RCP 4.5) | ~0.6m | 0.5 |
| $\omega_3$ | Pessimistic (RCP 8.5) | ~1.0m | 0.3 |

For each scenario, flood frequencies evolve according to Buchanan et al. (2017):

$$N_t^{(\omega)}(z) = \lambda \left[1 + \frac{\xi(z - \delta_t^{(\omega)} - \mu)}{\sigma}\right]^{-1/\xi}$$

Where $\delta_t^{(\omega)}$ is the sea-level rise in year $t$ under scenario $\omega$.

### 4.5 Solution Concept

We seek a **Subgame Perfect Nash Equilibrium (SPNE)** of the stochastic Stackelberg game:

1. **Homeowners** play their best response given local subsidy $S_j$
2. **Local governments** play their best response given federal policy $(\alpha, \bar{S})$ and anticipating homeowner responses
3. **Federal government** chooses $(\alpha^*, \bar{S}^*)$ anticipating both local and homeowner responses

**Solution Method:** Backward induction combined with Agent-Based Model simulation

```
Step 1: For each (α, S̄, ω), solve homeowner decisions via ABM
              ↓
Step 2: For each (α, S̄, ω), solve local government's best response
              ↓
Step 3: Aggregate across scenarios, find federal optimal (α*, S̄*)
```

---

## 5. Methodology

### 5.1 Overall Approach

```
┌────────────────────────────────────────────────────────────────┐
│                    METHODOLOGICAL FRAMEWORK                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│   ┌──────────────┐                                             │
│   │ Game Theory  │──── Stackelberg structure                   │
│   │              │──── Equilibrium analysis                    │
│   └──────┬───────┘                                             │
│          │                                                     │
│          ▼                                                     │
│   ┌──────────────┐                                             │
│   │  Stochastic  │──── Climate scenario modeling               │
│   │ Programming  │──── Expected value optimization             │
│   └──────┬───────┘──── Robust decision-making                  │
│          │                                                     │
│          ▼                                                     │
│   ┌──────────────┐                                             │
│   │  Agent-Based │──── Household heterogeneity                 │
│   │   Modeling   │──── Network effects                         │
│   └──────┬───────┘──── Dynamic relocation decisions            │
│          │                                                     │
│          ▼                                                     │
│   ┌──────────────┐                                             │
│   │    Equity    │──── Income-stratified outcomes              │
│   │   Analysis   │──── Distributional metrics                  │
│   └──────────────┘──── Policy counterfactuals                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 5.2 Agent-Based Model Component

Building on Zhou (2022), the ABM represents homeowner heterogeneity:

**Agent Attributes (from Zillow database):**
- Location (latitude, longitude, elevation)
- House market value
- Structure value (for damage calculation)
- Square footage
- Income proxy (based on house price percentile)

**Agent Decision Rule:**
```
For each year t:
    If not yet relocated:
        Calculate NPV of future expected flood damage
        Compare with (relocation cost - available subsidy)
        If NPV_damage > (M_h - S_j):
            Relocate
        Else:
            Stay and face flood risk
```

**Network Effects (optional extension):**
- Agents may be influenced by neighbors' relocation decisions
- If neighborhood vacancy rate exceeds threshold, relocation probability increases

### 5.3 Stochastic Programming Implementation

**Two-Stage Stochastic Program with Recourse:**

```
First Stage (Federal): Choose (α, S̄) before uncertainty resolves
                              ↓
                       Uncertainty Realized (ω)
                              ↓
Second Stage (Recourse): Local government and homeowners respond
```

**Implementation via Scenario Tree:**
```
                         t=0
                          │
                 ┌────────┼────────┐
                 │        │        │
               ω₁       ω₂       ω₃
            (RCP 2.6) (RCP 4.5) (RCP 8.5)
             p=0.2     p=0.5     p=0.3
                 │        │        │
                 ▼        ▼        ▼
           Local Gov  Local Gov  Local Gov
           Response   Response   Response
                 │        │        │
                 ▼        ▼        ▼
           Homeowner  Homeowner  Homeowner
           Decisions  Decisions  Decisions
```

### 5.4 Equity Metrics

We employ multiple metrics to assess distributional outcomes:

| Metric | Definition | Interpretation |
|--------|------------|----------------|
| **Relocation Ratio Gap** | $\frac{N_{low}^{relocate}/N_{low}^{total}}{N_{high}^{relocate}/N_{high}^{total}}$ | =1 is equitable; <1 means low-income underserved |
| **Subsidy Gini Coefficient** | Gini of subsidy distribution | Lower is more equitable |
| **Timing Gap** | $\bar{k}_{low}^* - \bar{k}_{high}^*$ | Average years low-income households relocate later |
| **Expected Damage Ratio** | $\frac{\mathbb{E}[D_{low}]}{\mathbb{E}[D_{high}]}$ | >1 means low-income bears more damage |

### 5.5 Computational Algorithm

```
Algorithm: Solve Stochastic Stackelberg Equilibrium

Input: Parameter values, climate scenarios Ω, household data
Output: Optimal (α*, S̄*), equilibrium outcomes

1. Initialize: α_grid = [0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1.0]
               S̄_grid = [0, 50K, 100K, ..., max_subsidy]

2. For each (α, S̄) in grid:
   3. For each scenario ω in Ω:
      4. Solve Local Government Best Response:
         - Given (α, S̄), find S_j* that minimizes local objective
         - Determine I_j* (apply or not)
      
      5. Run ABM:
         - Input: S_j*, household attributes
         - Simulate 80-year horizon
         - Output: k_h* for each household, damage trajectories
      
      6. Calculate outcomes for scenario ω:
         - Total federal cost
         - Total relocations by income group
         - Equity metrics
   
   7. Aggregate across scenarios:
      - Federal_Objective(α, S̄) = Σ_ω P(ω) · Cost(α, S̄, ω)
      - Equity_Metrics(α, S̄) = Σ_ω P(ω) · Equity(α, S̄, ω)

8. Find (α*, S̄*) = argmin Federal_Objective
   subject to Equity_Metrics ≥ threshold

9. Sensitivity Analysis:
   - Vary P(ω) distributions
   - Vary local government parameters (λ, r_L)
   - Vary homeowner discount rates

Return: (α*, S̄*), equilibrium outcomes, sensitivity results
```

---

## 6. Data Requirements

### 6.1 Data Sources Summary

| Data Category | Specific Data | Source | Status |
|---------------|---------------|--------|--------|
| **Household Data** | | | |
| House location | Latitude, longitude | Zillow ZTRAX | ✅ Available |
| House value | Total market value | Zillow ZTRAX | ✅ Available |
| Structure value | Improvement value | Zillow ZTRAX | ✅ Available |
| Elevation | Foundation height | USGS DEM | ✅ Available |
| **Flood Risk Data** | | | |
| Flood zones | 10-yr, 100-yr flood plains | FEMA NFHL | ✅ Available |
| Flood frequency parameters | λ, ξ, σ | Buchanan et al. (2017) | ✅ Available |
| Sea-level rise projections | RCP scenarios | Kopp et al. (2014) | ✅ Available |
| **Policy Parameters** | | | |
| Federal cost-share ratios | HMGP, BRIC rates | FEMA Policy Documents | ✅ Public |
| Historical buyout data | Past buyout counts, values | FEMA HMGP Database | ⚠️ Need to acquire |
| **Local Government Data** | | | |
| Property tax rates | By jurisdiction | NYC Dept. of Finance | ✅ Public |
| Local fiscal capacity | Budget data | Census of Governments | ⚠️ Need to acquire |
| **Damage Functions** | | | |
| Structure damage | By inundation depth | USACE (2003) | ✅ Available |
| Content damage | By inundation depth | FEMA (2019) | ✅ Available |

### 6.2 Case Study Area

**Primary Case Study: Brooklyn, NY (Three Zip Codes)**
- 11234 (Bergen Beach)
- 11235 (Sheepshead Bay)
- 11236 (Canarsie)

**Justification:**
- Variety of elevations (some in 10-yr flood plain, some above 100-yr)
- Mix of income levels
- Prior work provides validated parameters
- Includes census tracts classified as disadvantaged communities

**Sample Size:** ~1,143 one-story single-family homes

### 6.3 Parameter Values

| Parameter | Value | Source/Justification |
|-----------|-------|---------------------|
| **Discount Rates** | | |
| Federal ($r_F$) | 2.5% | Congressional Budget Office practice |
| Local ($r_L$) | 5-7% | Higher due to political cycles |
| High-income households ($r_R^{high}$) | 12% | Prior literature (Zhou 2022) |
| Low-income households ($r_R^{low}$) | 18% | Credit card debt rates (Traub 2014) |
| **Cost-Sharing** | | |
| Current federal share ($\alpha$) | 75% | FEMA HMGP standard |
| Range for analysis | 50-100% | Policy sensitivity |
| **Relocation Costs** | | |
| Base moving cost | $300,000 - $750,000 | Bishop (2007), Kennan & Walker (2011) |
| **Climate Scenarios** | | |
| RCP 2.6 probability | 0.2 | Author assumption |
| RCP 4.5 probability | 0.5 | Author assumption |
| RCP 8.5 probability | 0.3 | Author assumption |

---

## 7. Expected Contributions

### 7.1 Theoretical Contributions

1. **First multi-level government game model for flood buyouts**
   - Extends single-agent models (Bier et al. 2018) to strategic federal-local interaction
   - Provides equilibrium analysis of cost-sharing arrangements

2. **Integration of stochastic programming with Stackelberg games**
   - Accounts for climate uncertainty in policy optimization
   - Enables robust policy recommendations

3. **Formal equity framework for managed retreat**
   - Incorporates equity constraints into optimization
   - Provides theoretical basis for equity-efficiency trade-offs

### 7.2 Methodological Contributions

1. **Hybrid approach combining game theory and ABM**
   - Game theory for government interaction
   - ABM for heterogeneous household decisions
   - Computational tractability with behavioral realism

2. **Scenario-based analysis under deep uncertainty**
   - Transparent treatment of climate scenarios
   - Sensitivity to probability weights

### 7.3 Policy Contributions

1. **Evidence on optimal cost-sharing ratios**
   - Quantifies efficiency implications of different federal shares
   - Identifies potential for free-riding by local governments

2. **Equity impact assessment**
   - Documents how current policy affects income groups differently
   - Proposes alternative mechanisms to improve equity

3. **Specific policy recommendations**
   - Equity-weighted matching formulas
   - Sliding scale cost-shares based on community income
   - Minimum requirements for serving disadvantaged communities

### 7.4 Anticipated Findings (Hypotheses)

Based on theoretical reasoning, we anticipate:

| Hypothesis | Rationale |
|------------|-----------|
| **H1:** Higher federal cost-share increases buyout participation | Lower local cost burden |
| **H2:** Very high cost-shares (>90%) induce free-riding | Local governments wait for federal funds |
| **H3:** Current 75/25 split disadvantages low-income communities | Affluent areas more likely to apply |
| **H4:** Equity constraints reduce efficiency but are worthwhile | Trade-off is modest |
| **H5:** Climate uncertainty increases optimal cost-share | Precautionary motive |

---

## 8. Timeline and Milestones

### 8.1 Project Timeline (6 Months)

```
Month 1-2: Literature & Model Development
├── Week 1-2: Deep dive into fiscal federalism literature
├── Week 3-4: Formal model development and notation
├── Week 5-6: Mathematical proofs (existence of equilibrium)
└── Week 7-8: Model documentation and validation

Month 3: Data Collection & Preparation
├── Week 9-10: Acquire FEMA HMGP data, local fiscal data
├── Week 11-12: Data cleaning and integration
└── Deliverable: Complete dataset ready for analysis

Month 4: Computational Implementation
├── Week 13-14: Extend existing ABM code
├── Week 15-16: Implement Stackelberg game solver
└── Deliverable: Working computational model

Month 5: Analysis & Results
├── Week 17-18: Base case analysis
├── Week 19-20: Sensitivity analysis and robustness checks
└── Deliverable: Complete results

Month 6: Writing & Submission
├── Week 21-22: Draft manuscript
├── Week 23-24: Revisions and polishing
└── Deliverable: Manuscript ready for submission
```

### 8.2 Key Milestones

| Milestone | Target Date | Deliverable |
|-----------|-------------|-------------|
| M1: Literature review complete | End of Month 1 | Annotated bibliography |
| M2: Model formulation complete | End of Month 2 | Technical appendix with proofs |
| M3: Data ready | End of Month 3 | Cleaned dataset |
| M4: Code complete | End of Month 4 | Documented code repository |
| M5: Results complete | End of Month 5 | Tables and figures |
| M6: Manuscript submitted | End of Month 6 | Journal submission |

---

## 9. Target Journals

### 9.1 Primary Targets

| Journal | Impact Factor | Fit | Notes |
|---------|---------------|-----|-------|
| **Natural Hazards** | ~3.5 | ⭐⭐⭐⭐⭐ | Publishes game theory, ABM, policy analysis |
| **International Journal of Disaster Risk Reduction** | ~5.0 | ⭐⭐⭐⭐⭐ | Strong policy relevance focus |
| **Climate Risk Management** | ~5.0 | ⭐⭐⭐⭐ | Emphasizes decision-making under uncertainty |

### 9.2 Secondary Targets

| Journal | Impact Factor | Fit | Notes |
|---------|---------------|-----|-------|
| **Risk Analysis** | ~4.0 | ⭐⭐⭐⭐ | If strong methodological contribution |
| **Journal of Flood Risk Management** | ~3.0 | ⭐⭐⭐⭐ | Specialized audience |
| **Climatic Change** | ~5.0 | ⭐⭐⭐ | Broader climate focus |

### 9.3 Submission Strategy

```
Round 1: Submit to Natural Hazards or IJDRR
         ↓
    If rejected
         ↓
Round 2: Revise and submit to Climate Risk Management
         ↓
    If rejected
         ↓
Round 3: Submit to Journal of Flood Risk Management
```

---

## 10. References

### Foundational Works (Prior Research by Authors)

- Bier, V. M., Zhou, Y., & Du, H. (2018). Game-theoretic modeling of pre-disaster relocation. *The Engineering Economist*, 65(2), 89-113.

- Zhou, Y. (2022). Pre-disaster relocation and Agent-based model for Flood Disaster. *Doctoral Dissertation*, University of Wisconsin-Madison.

### Multi-Level Government and Fiscal Federalism

- Oates, W. E. (1999). An essay on fiscal federalism. *Journal of Economic Literature*, 37(3), 1120-1149.

- Sigman, H. (2005). Transboundary spillovers and decentralization of environmental policies. *Journal of Environmental Economics and Management*, 50(1), 82-101.

- Slavikova, L. (2018). Effects of government flood expenditures: The problem of crowding-out. *Journal of Flood Risk Management*, 11(1), 95-104.

### Game Theory in Disaster Management

- Guan, P., & Zhuang, J. (2015). Modeling public–private partnerships in disaster management via centralized and decentralized models. *Decision Analysis*, 12(4), 173-189.

- Hausken, K., & Zhuang, J. (2016). The strategic interaction between a company and the government surrounding disasters. *Annals of Operations Research*, 237(1), 27-40.

- Jeong, H., Ha, S., & Kim, H. (2018). Flood protection cost allocation using cooperative game theory for adapting infrastructure to climate change. *Journal of Water Resources Planning and Management*, 144(4), 04018010.

### Managed Retreat and Buyouts

- Elliott, J. R., Brown, P. L., & Loughran, K. (2021). Racial inequities in the federal buyout of flood-prone homes: A nationwide assessment of environmental adaptation. *Socius*, 6, 1-5.

- Freudenberg, R., Calvin, E., Tolkoff, L., & Brawley, D. (2016). Buy-in for buyouts: The case for managed retreat from flood zones. *Lincoln Institute of Land Policy*.

- Kousky, C., Fleming, B., & Berger, A. M. (Eds.). (2021). *A Blueprint for Coastal Adaptation: Uniting Design, Economics, and Policy*. Island Press.

- Mach, K. J., et al. (2019). Managed retreat through voluntary buyouts of flood-prone properties. *Science Advances*, 5(10), eaax8995.

- Marino, E. (2018). Adaptation privilege and voluntary buyouts: Perspectives on ethnocentrism in sea level rise relocation and retreat policies in the US. *Global Environmental Change*, 49, 10-13.

- Siders, A. R., Hino, M., & Mach, K. J. (2019). The case for strategic and managed climate retreat. *Science*, 365(6455), 761-763.

### Stochastic Programming and Climate Uncertainty

- Giuliani, M., & Castelletti, A. (2016). Is robustness really robust? How different definitions of robustness impact decision-making under climate change. *Climatic Change*, 135(3-4), 409-424.

- Hecht, J. S., & Kirshen, P. H. (2019). Minimizing urban floodplain management regrets under deeply uncertain climate change. *Journal of Water Resources Planning and Management*, 145(2), 04018096.

- Hinkel, J., et al. (2019). Meeting user needs for sea level rise information: A decision analysis perspective. *Earth's Future*, 7(3), 320-337.

### Flood Risk and Sea-Level Rise

- Buchanan, M. K., Kopp, R. E., Oppenheimer, M., & Tebaldi, C. (2016). Allowances for evolving coastal flood risk under uncertain local sea-level rise. *Climatic Change*, 137(3), 347-362.

- Kopp, R. E., et al. (2014). Probabilistic 21st and 22nd century sea-level projections at a global network of tide-gauge sites. *Earth's Future*, 2(8), 383-406.

### Behavioral Economics and Discounting

- Kunreuther, H. C., Pauly, M. V., & McMorrow, S. (2013). *Insurance and Behavioral Economics: Improving Decisions in the Most Misunderstood Industry*. Cambridge University Press.

- Traub, A. (2014). What drives credit card debt in America. *Demos*.

---

## Appendix A: Preliminary Results from Prior Work

The following results from Zhou (2022) provide a foundation for this research:

### A.1 Base Case Results (Brooklyn, NY)

| Metric | $300K Relocation Cost | $750K Relocation Cost |
|--------|----------------------|----------------------|
| Optimal subsidy | $200,000 | $610,000 |
| Government objective value | $4.31 × 10⁸ | $7.85 × 10⁸ |
| Households relocating | 848 (74%) | 843 (74%) |
| Free riders | 495 (43%) | 374 (33%) |

### A.2 Key Sensitivity Findings

- Government discount rate has moderate impact on optimal subsidy
- **Resident discount rate has large impact** — higher discount rates require larger subsidies
- Targeting subsidies to low-income households reduces both costs and free-riding

### A.3 Equity-Related Finding

Restricting subsidies to houses below $700,000 reduces:
- Government costs by 24%
- Number of free riders by 80%

This suggests **income-based targeting improves both efficiency and equity**.

---

## Appendix B: Model Extensions (Future Work)

The following extensions could be pursued in subsequent research:

1. **Dynamic game with learning**: Governments update beliefs about climate as evidence accumulates

2. **Multiple local governments**: Spatial spillovers and competition for federal funds

3. **Insurance market integration**: Three-way interaction between government, insurers, and households

4. **Political economy**: Electoral cycles affecting local government discount rates

---

*End of Research Proposal*