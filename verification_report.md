# Mathematical and Numerical Verification Report

**File**: `D:\Github\Equity-Implications-of-Federal-Local-Cost-sharing-in-Flood-Buyouts\paper\arxiv\main.tex`
**Date**: 2026-01-29

---

## PART 1: NUMERICAL ERRORS AND INCONSISTENCIES

### ERROR #1: Income Group Household Counts (CRITICAL)

**Location**: Line 121
**Issue**: Household counts by income group do not match Table 1 calculations

**From Table 1** (Lines 512-520), calculating with regional low-income shares:

| Region | Total HH | Low-Income % | Low-Income HH |
|--------|----------|--------------|---------------|
| Brooklyn | 5,200 | 45% | 2,340 |
| Staten Island | 2,800 | 52% | 1,456 |
| Queens | 4,100 | 58% | 2,378 |
| Lower Manhattan | 1,850 | 15% | 277.5 |
| Houston | 6,500 | 55% | 3,575 |
| New Orleans | 4,200 | 62% | 2,604 |
| Miami-Dade | 5,100 | 48% | 2,448 |
| Charleston | 2,350 | 42% | 987 |
| Norfolk | 2,393 | 50% | 1,196.5 |
| **TOTAL** | **34,493** | - | **17,262** |

**High-income households**: 34,493 - 17,262 = **17,231**

**Text claims** (Line 121):
- Low-income: 17,123 households ❌ **ERROR**: Should be 17,262 (139 fewer)
- High-income: 17,370 households ❌ **ERROR**: Should be 17,231 (139 more)

**Impact**: This affects the denominators in all relocation rate calculations.

---

### ERROR #2: RRG (Relocation Ratio Gap) Value (CRITICAL)

**Location**: Lines 121, 192, Abstract (Line 73), Figure caption (Line 539)
**Issue**: RRG calculation does not match stated value

**Using text's own numbers** (17,123 and 17,370):
- Low-income rate: 191/17,123 = 0.01116 = 1.12%
- High-income rate: 693/17,370 = 0.03990 = 3.99%
- **RRG = 0.01116 / 0.03990 = 0.280**

**Text consistently claims**: RRG = 0.26

**Discrepancy**: |0.28 - 0.26| / 0.28 = **7.1% relative error**

This is a **CRITICAL** error as RRG is the main outcome metric throughout the paper. The value 0.26 appears in:
- Abstract (Line 73)
- Main results (Line 121)
- Figure 1 caption (Line 539)
- Multiple other locations

**Impact**: Overstates the inequity of current policy by ~7%.

---

### ERROR #3: Percentage Rounding (MINOR - Actually Correct)

**Location**: Line 121

Text states:
- "191 of 17,123 low-income households (1.1%)"
- "693 of 17,370 high-income households (4.0%)"

**Actual calculations**:
- 191/17,123 = 1.116% → rounds to 1.1% ✓
- 693/17,370 = 3.990% → rounds to 4.0% ✓

**Assessment**: Percentages are correctly rounded.

---

## PART 2: MATHEMATICAL FORMULA ERRORS

### ERROR #4: Theorem 1 Index Inconsistency (MODERATE)

**Location**: Lines 402-427 (Appendix)
**Issue**: Index mismatch between theorem statement and proof

**Theorem statement** (Line 405):
```
E_ω[D_{h,k}^(ω)] ≥ (M_h - S) · r_h
```
Uses D_{h,k} (damage in year k)

**Proof conclusion** (Lines 423-424):
```
E_ω[D_{h,k-1}^(ω)] = (M_h - S) · r_h
```
Uses D_{h,k-1} (damage in year k-1)

**Correct form**: The optimal year k* satisfies:
```
E_ω[D_{h,k-1}^(ω)] ≥ (M_h - S) · r_h
```

This is because you relocate in year k when damage in the CURRENT year (year k-1, before relocating) exceeds annualized relocation cost.

**Impact**: Theorem statement should use D_{h,k-1} not D_{h,k}.

---

### ERROR #5: Discrete Optimization Notation Issue (MODERATE)

**Location**: Lines 410-427 (Appendix, Theorem 1 proof)
**Issue**: Taking continuous derivative of discrete optimization problem

The proof states (Line 416):
> "The first-order condition ∂C_h/∂k = 0 yields..."

**Problem**: k is the relocation YEAR (discrete integer variable), not continuous.

The proof then writes (Line 417):
```
-((M_h - S)·ln(1+r_h))/(1+r_h)^k + E_ω[D_{h,k-1}^(ω)]/(1+r_h)^{k-1} = 0
```

**Issues**:
1. Treating k as continuous allows taking ∂/∂k, but k ∈ {0,1,2,...,T}
2. The derivative d/dk[(1+r_h)^k] = (1+r_h)^k · ln(1+r_h) is correct for continuous k
3. The summation bound change when k increases is not properly handled in continuous derivative

**Correct approach**: Compare C_h(k) vs C_h(k-1) and find when C_h(k) < C_h(k-1)

**Impact**: Result is correct but derivation method is imprecise for discrete optimization.

---

### ERROR #6: Theorem 2 Dimensional Inconsistency (CRITICAL)

**Location**: Lines 432-436 (Appendix, Theorem 2)
**Issue**: Formula is dimensionally inconsistent

**Theorem 2 states** (Lines 433-435):
```
S_j* = min{S̄, [(1-α) + λ_j·τ_j] / [∂N_j^rel/∂S_j · ((1-α) + λ_j·τ_j·V_j^avg) - ∂E[C_j^loc]/∂S_j]}
```

**Problem**:
- Numerator = (1-α) + λ_j·τ_j
  - α is dimensionless [0,1]
  - τ_j is tax rate (dimensionless, e.g., 0.01 for 1%)
  - **Numerator is DIMENSIONLESS**

- But S_j* is a subsidy with units of **DOLLARS**

A dimensionless numerator divided by any denominator cannot yield dollars.

**This suggests**:
1. The formula is a stylized representation, not the literal FOC solution
2. There are missing terms or dimensional constants
3. The proof (Lines 439-446) only says "Taking FOC and solving" without showing actual algebra, which hides this issue

**Impact**: Formula cannot be used for actual calculations as written. Appears to be conceptual/illustrative rather than operational.

---

### ERROR #7: Equation (3) Double Expectation Notation (MODERATE)

**Location**: Lines 203-205 (Methods section, Equation 3)
**Issue**: Redundant or undefined double expectation

**Equation (3) shows**:
```
C_h(k) = (M_h - S_j)/(1+r_h)^{k_h} + Σ_{t=0}^{k_h-1} E_ω[E[D_{h,t}^(ω)]]/(1+r_h)^t
```

The notation **E_ω[E[D_{h,t}^(ω)]]** has two expectation operators:

**Option 1**: If they represent the same operation (expectation over climate scenarios ω), then one is redundant. Should be: **E_ω[D_{h,t}^(ω)]**

**Option 2**: If they represent different operations:
- Outer E_ω[·]: expectation over climate scenarios
- Inner E[·]: expectation over some other randomness
- But what is this other randomness? **Not defined in the paper.**

**Additionally**: The formula uses k_h as both subscript and the variable being optimized over (see line 202: "chooses relocation year k_h"). This creates notational ambiguity.

**Impact**: Notation is unclear and potentially confusing to readers.

---

### ERROR #8: Undefined Variable C_j^Fed (MINOR)

**Location**: Line 192 (Equation 1)
**Issue**: Variable C_j^Fed appears but is never defined

**Equation (1)**:
```
min E_ω[Σ_j α·S_j*·N_j^rel + C_j^Fed]
```

The term **C_j^Fed** is not defined in the Methods section.

**Likely interpretation**: Federal costs beyond direct subsidy payments (e.g., FEMA administrative costs)

**Impact**: Minor - doesn't affect numerical results, but should be defined for completeness.

---

## PART 3: VERIFIED CORRECT ELEMENTS

### ✓ Total Household Count
- Sum from Table 1: 5,200+2,800+4,100+1,850+6,500+4,200+5,100+2,350+2,393 = **34,493** ✓
- Matches text claims throughout the paper

### ✓ Federal Cost Fold Increase
- Text (Line 123): "increases from $82 million to $375 million—a 4.6-fold increase"
- Calculation: 375/82 = 4.573 ≈ 4.6 ✓
- Correctly rounded

### ✓ Theorem 3 Existence Proof
- Lines 450-462: Structure is mathematically sound
- Uses backward induction (standard for Stackelberg games)
- Invokes Weierstrass theorem (correct for compact sets)
- Properly establishes existence at each stage
- No errors detected ✓

### ✓ Table 1 Regional Parameters
- Table 1 (Lines 503-526) appears internally consistent with descriptions in main text (Lines 118-119)
- Values are plausible and well-documented

---

## SUMMARY OF ERRORS

### CRITICAL ERRORS (require correction):
1. **Income group household counts** (17,123 vs 17,262; 17,370 vs 17,231)
2. **RRG value** (0.26 vs 0.28) - appears throughout paper
3. **Theorem 2 dimensional inconsistency**

### MODERATE ERRORS (should be corrected for clarity):
4. Theorem 1 index inconsistency (D_k vs D_{k-1})
5. Discrete optimization notation in Theorem 1 proof
6. Double expectation notation in Equation (3)

### MINOR ERRORS (low priority):
7. Undefined variable C_j^Fed

### VERIFIED CORRECT:
- Total household count (34,493) ✓
- Federal cost fold increase (4.6×) ✓
- Theorem 3 existence proof structure ✓
- Table 1 regional parameters ✓

---

## RECOMMENDATIONS

1. **Recalculate income group totals** using Table 1 percentages
   - Update all instances of 17,123 → 17,262 and 17,370 → 17,231

2. **Recalculate and verify RRG** throughout paper
   - If true value is 0.28, update all instances of 0.26 → 0.28
   - Alternative: Check if simulation data supports 0.26, then adjust household counts accordingly

3. **Revise Theorem 2** to either:
   - Provide complete FOC solution with proper dimensions, OR
   - Clarify it's a stylized representation for intuition

4. **Fix Theorem 1** to use D_{k-1} consistently in both statement and proof

5. **Clarify Equation (3)** expectation notation - use single E_ω[·]

6. **Define C_j^Fed** in Methods section

7. **Consider using discrete optimization notation** (difference equations) rather than continuous derivatives for integer year k
