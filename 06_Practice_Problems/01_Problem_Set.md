# Practice Problems: Finite Element Method

## Problem Set 1: Basic 1D Bar Problems

These problems help reinforce fundamental FEM concepts. Start with Problem 1 and progress through the set.

---

## Problem 1 ⭐ - Simple Tension Test

### Problem Statement

A uniform aluminum bar is subjected to a tensile load. Analyze using FEM with 2 elements.

```
         F = 50 kN
             ↓
Fixed ├─────────────┤ Free
      0    0.5m   1.0m

Material Properties:
  E = 70 GPa (Aluminum)
  A = 500 mm²

Boundary Conditions:
  Left end: fixed (u = 0)
  Right end: applied load F = 50 kN
```

### Required Calculations

1. Calculate element stiffness matrices
2. Assemble global stiffness matrix
3. Apply boundary conditions
4. Solve for all nodal displacements
5. Calculate stresses in each element
6. Find reaction force at fixed support
7. Compare with analytical solution

### Hints

- Number of nodes: 3
- Element length: L = 0.5 m (each)
- Stiffness formula: [K]ᵉ = (EA/L) × [1 -1; -1 1]
- For uniform bar, EA/L is the same for both elements

### Expected Results Range

| Parameter | Expected Value |
|-----------|-----------------|
| u₂ | ~1.4 × 10⁻⁴ m |
| u₃ | ~2.9 × 10⁻⁴ m |
| σ₁, σ₂ | ~100 MPa |
| Reaction | ~50 kN |

### Solution Approach

1. **Setup**: Identify element connectivity, material properties
2. **Element Matrices**: Calculate k₁ = EA/L for 0.5 m element
3. **Assembly**: Direct stiffness method, add contributions
4. **Boundary Condition**: Remove equation for u₁ = 0
5. **Solution**: Solve 2×2 system for u₂, u₃
6. **Post-Process**: σ = E(u₂-u₁)/L

---

## Problem 2 ⭐ - Heat Conduction in a Rod

### Problem Statement

A composite rod with different thermal conductivities experiences steady-state heat conduction. Find temperature distribution.

```
T₁ = 100°C        Heat sink (q = 0)
  ├─────────────────┤
  │  Material 1     │
  ├─────────────────┤
  │  Material 2     │
  └─────────────────┘
                T₃ = 20°C

Dimensions:
  L₁ = 0.5 m, k₁ = 50 W/(m·K)
  L₂ = 0.5 m, k₂ = 100 W/(m·K)

Boundary Conditions:
  T₁ = 100°C (fixed temperature)
  T₃ = 20°C (fixed temperature)
```

### Required Calculations

1. Set up heat conduction finite element equation: [K]{T} = {Q}
2. Element stiffness: [K]ᵉ = (k/L) × [1 -1; -1 1]
3. Assemble global system
4. Apply Dirichlet BCs (T₁ = 100, T₃ = 20)
5. Solve for T₂
6. Calculate heat flux in each element
7. Verify heat balance (q_in = q_out)

### Element Equations

For 1D heat conduction:
```
d/dx(k·dT/dx) = Q

Stiffness: [K]ᵉ = (k/L) [1  -1]
                         [-1  1]
```

### Expected Results Range

| Parameter | Expected Value |
|-----------|-----------------|
| T₂ | ~43°C - 50°C |
| q₁ | ~50 W/m |
| q₂ | ~40 W/m |

### Verification

Heat flow continuity: q₁ = q₂ (through series elements)

---

## Problem 3 ⭐ - Cantilever Beam with Point Load

### Problem Statement

A cantilever beam fixed at one end carries a point load at the free end. Use 2 beam elements.

```
Fixed support        Point load P = 10 kN
├──────────────────────┤─ ← deflection v
               v       ↓
 ├─────────────────────┤
 x = 0                x = L = 2 m

Material: Steel
  E = 200 GPa
  I = 100 cm⁴ = 100 × 10⁻⁸ m⁴

Boundary Conditions:
  At x = 0: v = 0, θ = 0 (fixed)
  At x = 2m: P = 10 kN (downward)
```

### Required Calculations

1. Beam element stiffness (3 DOF per node: v, θ, not applicable)
2. 2D DOF per element (or use structure with 2 elements)
3. Assembly with appropriate connectivity
4. Apply boundary conditions
5. Solve for free-end deflection v₃
6. Calculate slopes at nodes
7. Calculate bending moments M = EI(d²v/dx²)
8. Verify with analytical solution: v_tip = PL³/(3EI)

### Beam Element Stiffness

```
          [ 12   6L  -12   6L ]
[K]ᵉ = (EI/L³) [ 6L  4L²  -6L  2L² ]
          [-12  -6L   12  -6L ]
          [ 6L  2L²  -6L  4L² ]
```

Where:
- Nodal DOF: [v₁, θ₁, v₂, θ₂]
- L = 1 m (each element, since total length 2 m)

### Expected Results Range

| Parameter | Expected Value |
|-----------|-----------------|
| v₃ | ~-5 mm |
| Analytical v₃ | PL³/(3EI) = 2.5 mm |
| Bending moment | ~10 kN·m |

### Analytical Verification

```
v_max = PL³/(3EI) = (10×10³ × 2³) / (3 × 200×10⁹ × 100×10⁻⁸)
      = 80,000 / (3 × 2000)
      = 80,000 / 6000
      ≈ 13.3 mm
```

---

## Problem 4 ⭐ - Stepped Bar in Tension

### Problem Statement

A stepped steel bar with varying cross-section is loaded at the ends. Determine stresses in each section and maximum displacement.

```
        F = 200 kN
             ↓
    A₁          A₂
├─────────┼─────────┤
Node 1   2        3
(fixed)  

Section 1 (0 to 1m):
  A₁ = 200 mm²
  E = 200 GPa

Section 2 (1m to 2m):
  A₂ = 100 mm² (narrower)
  E = 200 GPa
```

### Required Calculations

1. Setup connectivity (2 elements, 3 nodes)
2. Calculate element stiffness: k = EA/L
3. Note: Different stiffness values!
4. Assemble global system [K] with 3×3 dimension
5. Apply u₁ = 0 (fixed) and F₃ = 200 kN
6. Solve for u₂ and u₃
7. Calculate stresses: σ = E·(u₂-u₁)/L
8. Identify stress concentration (stress is higher in narrower section)

### Key Insight

Same force, different areas → different stresses
```
σ₁ = F/A₁ = 200 kN / 200 mm² = 1000 MPa
σ₂ = F/A₂ = 200 kN / 100 mm² = 2000 MPa
```

### Expected Results Range

| Parameter | Expected Value |
|-----------|-----------------|
| u₂ | ~5.0 × 10⁻³ m |
| u₃ | ~10.0 × 10⁻³ m |
| σ₁ | ~1000 MPa |
| σ₂ | ~2000 MPa |

### Critical Issue

The narrower section has twice the stress! This is a stress concentration that requires careful design consideration.

---

## Problem 5 ⭐ - Composite Material Bar

### Problem Statement

A composite bar made of two different materials experiences tensile loading. Determine displacement and stress distribution.

```
          F = 100 kN
              ↓
Material 1  Material 2
├─────────┼─────────┤
Node 1   2        3

Material 1: Aluminum
  E₁ = 70 GPa
  A₁ = 300 mm²
  L₁ = 1.0 m

Material 2: Steel
  E₂ = 200 GPa
  A₂ = 300 mm²
  L₂ = 1.0 m
```

### Required Calculations

1. Element 1 stiffness: k₁ = E₁A₁/L₁
2. Element 2 stiffness: k₂ = E₂A₂/L₂
3. Assemble with different material properties
4. Note: k₂ > k₁ (steel stiffer than aluminum)
5. Solve for displacements u₂, u₃
6. Calculate strains: ε = (u₂-u₁)/L
7. Calculate stresses: σ = E·ε
8. Compare strain distribution

### Strain and Stress Analysis

For same area but different E:
```
Same force → different strains
ε₁ = σ/E₁ = σ/70 GPa
ε₂ = σ/E₂ = σ/200 GPa

ε₁ > ε₂ (aluminum deforms more for same stress)
```

### Expected Results Range

| Parameter | Element 1 (Al) | Element 2 (Steel) |
|-----------|----------------|-------------------|
| ε | ~4.8 × 10⁻³ | ~1.67 × 10⁻³ |
| σ | ~336 MPa | ~334 MPa |
| ΔL | ~4.8 mm | ~1.67 mm |

### Physical Insight

Material with lower E is more compliant and deforms more, even though both carry same force.

---

## Submission Template

For each problem, provide:

```
PROBLEM X: [PROBLEM NAME]

1. SETUP
   - Number of nodes: ___
   - Number of elements: ___
   - Total DOF: ___
   - Element type: ___

2. ELEMENT MATRICES
   Element 1:
   [K]¹ = ___
   
   Element 2:
   [K]² = ___

3. GLOBAL SYSTEM
   [K]ᵍˡᵒᵇᵃˡ = [___]

4. BOUNDARY CONDITIONS
   Applied: ___
   Reaction: ___

5. SOLUTION
   {u} = {___}
   {R} = {___}

6. POST-PROCESSING
   Stresses: σ = ___
   Strains: ε = ___
   Other: ___

7. VERIFICATION
   Analytical vs. FEM: ___
   Error: ___

8. CONCLUSIONS
   Key observations: ___
```

---

## Solution Strategy Guidelines

### For 1D Bar Problems

1. **Stiffness**: k = EA/L
2. **Assembly**: Add contributions to global K
3. **BC**: Set known DOF, solve for unknowns
4. **Stress**: σ = E × ε = E × (Δu/L)
5. **Verify**: Check force balance: ΣF = 0

### For 1D Heat Transfer

1. **Thermal Stiffness**: k = κ/L (κ = thermal conductivity)
2. **Heat Source**: Q distributed or concentrated
3. **Temperature BC**: T_fixed applied
4. **Heat Flux**: q = -κ(dT/dx)
5. **Verify**: Heat in = Heat out

### For Beam Elements

1. **DOF per Node**: 2 (deflection, slope)
2. **Element K**: 4×4 matrix (use formula from Module 3)
3. **Boundary**: Fixed = v = θ = 0
4. **Load**: Concentrated or distributed
5. **Moment**: M = EI(d²v/dx²)

---

## Difficulty Levels

**⭐ Basic**: Understand FEM procedure, simple linear algebra  
**⭐⭐ Intermediate**: Multiple materials, coupled effects  
**⭐⭐⭐ Advanced**: Nonlinear, time-dependent, optimization  

---

## Resources for Solving

- [03_Key_Equations.md](../03_Key_Equations.md) - Formula reference
- [01_Simple_Truss.md](./01_Simple_Truss.md) - Worked example
- [04_Code_Examples/01_1D_Bar_Element.py](../04_Code_Examples/01_1D_Bar_Element.py) - Python implementation
- [02_Theory.md](../02_Theory.md) - Mathematical foundations

---

## Next Steps

1. ✓ Complete all 5 basic problems
2. ✓ Check solutions against provided answers
3. ✓ Run Python code for problems 1, 4, 5
4. ✓ Create plots of results
5. ✓ Write brief analysis of physical behavior
6. → Ready for advanced problems!

---

**Solutions available in → [02_Solutions.md](./02_Solutions.md)**
