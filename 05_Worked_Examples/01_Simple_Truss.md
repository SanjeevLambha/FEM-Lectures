# Worked Example 1: Two-Element Truss Analysis

## Problem Statement

Analyze a simple two-element stepped bar subject to axial loading and determine:
1. Nodal displacements
2. Element stresses and strains
3. Reaction forces
4. Internal load distribution

### Geometry and Loading

```
                  Load P = 100 kN
                     ↓
Elem 1: A₁, E, L₁  Elem 2: A₂, E, L₂
├─────────────┼─────────────┤
Node 1      Node 2      Node 3
(Fixed)     (Free)      (Loaded)

Material Properties:
  E = 200 GPa (Young's modulus - same for both elements)
  
Element 1:
  A₁ = 100 mm² = 100 × 10⁻⁶ m²
  L₁ = 1.0 m
  
Element 2:
  A₂ = 200 mm² = 200 × 10⁻⁶ m²
  L₂ = 1.0 m

Applied Load:
  P = 100 kN = 100 × 10³ N at node 3

Boundary Conditions:
  u₁ = 0 (fixed at node 1)
```

---

## Step-by-Step Solution

### Step 1: Problem Discretization and Unknowns

**System Definition**:
- Number of nodes: 3
- Number of elements: 2
- Number of DOF per node: 1 (axial displacement)
- Total system DOF: 3

**Element Connectivity**:
| Element | Local Nodes | Global Nodes | Node 1 | Node 2 |
|---------|------------|--------------|--------|--------|
| 1 | 1, 2 | 1, 2 | u₁ | u₂ |
| 2 | 1, 2 | 2, 3 | u₂ | u₃ |

**Unknowns to Find**:
- u₂ = displacement at node 2
- u₃ = displacement at node 3
- R₁ = reaction force at node 1

---

### Step 2: Element Stiffness Matrices

**Stiffness Formula for Bar Element**:
```
[K]ᵉ = (EA/L) [ 1  -1]
              [-1   1]
```

**Element 1**:
```
k₁ = E₁A₁/L₁ = (200 × 10⁹ Pa)(100 × 10⁻⁶ m²) / (1.0 m)
   = 200 × 10⁹ × 100 × 10⁻⁶ / 1
   = 20 × 10⁶ N/m
   = 20 MN/m

[K]¹ = 20 × 10⁶ [ 1  -1] N/m
                 [-1   1]

[K]¹ = [20×10⁶   -20×10⁶] N/m
       [-20×10⁶   20×10⁶]
```

**Element 2**:
```
k₂ = E₂A₂/L₂ = (200 × 10⁹ Pa)(200 × 10⁻⁶ m²) / (1.0 m)
   = 200 × 10⁹ × 200 × 10⁻⁶ / 1
   = 40 × 10⁶ N/m
   = 40 MN/m

[K]² = 40 × 10⁶ [ 1  -1] N/m
                 [-1   1]

[K]² = [40×10⁶   -40×10⁶] N/m
       [-40×10⁶   40×10⁶]
```

---

### Step 3: Global Stiffness Matrix Assembly

**Assembly Procedure** (Direct Stiffness Method):

**Element 1** connects global nodes 1-2:
```
K(1,1) += K¹(1,1) = 20×10⁶
K(1,2) += K¹(1,2) = -20×10⁶
K(2,1) += K¹(2,1) = -20×10⁶
K(2,2) += K¹(2,2) = 20×10⁶
```

**Element 2** connects global nodes 2-3:
```
K(2,2) += K²(1,1) = +40×10⁶
K(2,3) += K²(1,2) = -40×10⁶
K(3,2) += K²(2,1) = -40×10⁶
K(3,3) += K²(2,2) = 40×10⁶
```

**Resulting Global Stiffness Matrix**:
```
[K]ᵍˡᵒᵇᵃˡ = [ 20    -20      0  ] × 10⁶  (N/m)
             [-20   (20+40)  -40]
             [  0    -40      40]

[K]ᵍˡᵒᵇᵃˡ = [ 20   -20     0 ] × 10⁶  (N/m)
             [-20    60   -40]
             [  0   -40    40]
```

**Verification of Connectivity**:
- Diagonal: All positive ✓
- Symmetry: Kᵢⱼ = Kⱼᵢ ✓

---

### Step 4: Load Vector

**Applied Loads**:
- Node 1: No applied load → F₁ = 0
- Node 2: No applied load → F₂ = 0
- Node 3: Applied load P = 100 kN → F₃ = 100,000 N

**Global Load Vector**:
```
{F} = { 0     }  N
      { 0     }
      {100,000}
```

---

### Step 5: System Equations Before Boundary Conditions

**Unmodified System**:
```
[K]{u} = {F}

[ 20   -20     0 ] × 10⁶  { u₁ }   {    0     }
[-20    60   -40]          { u₂ } = {    0     }
[  0   -40    40]          { u₃ }   {100,000   }
```

---

### Step 6: Apply Boundary Conditions

**Essential Boundary Condition**:
```
u₁ = 0 (fixed support at node 1)
```

**Method: Direct Elimination**

Remove row 1 and column 1 from system:

**Reduced System**:
```
[ 60   -40] × 10⁶  { u₂ }   {    0     }
[-40    40]          { u₃ } = {100,000   }
```

---

### Step 7: Solve for Displacements

**Reduced System**:
```
60×10⁶·u₂ - 40×10⁶·u₃ = 0          ... (1)
-40×10⁶·u₂ + 40×10⁶·u₃ = 100,000   ... (2)
```

**From Equation (1)**:
```
60×10⁶·u₂ = 40×10⁶·u₃
u₂ = (40/60)·u₃ = (2/3)·u₃         ... (3)
```

**Substitute into Equation (2)**:
```
-40×10⁶·(2/3)·u₃ + 40×10⁶·u₃ = 100,000
-80/3 × 10⁶·u₃ + 40×10⁶·u₃ = 100,000
(-80/3 + 40/1) × 10⁶·u₃ = 100,000
(-80/3 + 120/3) × 10⁶·u₃ = 100,000
(40/3) × 10⁶·u₃ = 100,000
u₃ = 100,000 × 3 / (40 × 10⁶)
u₃ = 300,000 / (40 × 10⁶)
u₃ = 0.0075 m = 7.5 × 10⁻³ m
```

**From Equation (3)**:
```
u₂ = (2/3) × 0.0075
u₂ = 0.005 m = 5.0 × 10⁻³ m
```

**Verification with Equation (2)**:
```
-40×10⁶ × 0.005 + 40×10⁶ × 0.0075
= -200,000 + 300,000
= 100,000 ✓ (matches applied load)
```

**Nodal Displacements**:
```
u₁ = 0 m (fixed)
u₂ = 5.0 × 10⁻³ m = 5.0 mm
u₃ = 7.5 × 10⁻³ m = 7.5 mm
```

---

### Step 8: Post-Processing - Stresses and Strains

**Element 1** (Nodes 1-2):

**Strain**:
```
ε₁ = (u₂ - u₁) / L₁
   = (5.0×10⁻³ - 0) / 1.0
   = 5.0×10⁻³
   = 0.005
```

**Stress**:
```
σ₁ = E × ε₁
   = 200×10⁹ × 5.0×10⁻³
   = 1.0×10⁹ Pa
   = 1000 MPa
```

**Internal Force**:
```
N₁ = σ₁ × A₁
   = 1000×10⁶ × 100×10⁻⁶
   = 100×10³ N
   = 100 kN
```

---

**Element 2** (Nodes 2-3):

**Strain**:
```
ε₂ = (u₃ - u₂) / L₂
   = (7.5×10⁻³ - 5.0×10⁻³) / 1.0
   = 2.5×10⁻³
   = 0.0025
```

**Stress**:
```
σ₂ = E × ε₂
   = 200×10⁹ × 2.5×10⁻³
   = 0.5×10⁹ Pa
   = 500 MPa
```

**Internal Force**:
```
N₂ = σ₂ × A₂
   = 500×10⁶ × 200×10⁻⁶
   = 100×10³ N
   = 100 kN
```

---

### Step 9: Reaction Force Calculation

**Method**: Use full system equation
```
[K]ᵍˡᵒᵇᵃˡ {u} = {F} + {R}

where {R} = reaction forces
```

**Full solution vector**:
```
{u} = { 0      }
      { 0.005  }
      { 0.0075 }
```

**Calculate [K]{u}**:
```
[ 20   -20     0 ] × 10⁶  {   0   }   [ 20×0 + (-20)×0.005 + 0×0.0075 ]
[-20    60   -40]          { 0.005 } = [(-20)×0 + 60×0.005 + (-40)×0.0075]
[  0   -40    40]          { 0.0075}   [ 0×0 + (-40)×0.005 + 40×0.0075 ]

= [ -100,000   ]
  [   0        ]
  [  100,000   ]
```

**Reaction vector**:
```
{R} = [K]{u} - {F}

R₁ = -100,000 - 0 = -100,000 N = -100 kN (reaction upward)
R₂ = 0 - 0 = 0 N (no external load at node 2)
R₃ = 100,000 - 100,000 = 0 N ✓
```

**Verification**:
```
Sum of external and reaction forces:
F_total = R₁ + F₃ = -100,000 + 100,000 = 0 ✓ (equilibrium satisfied)
```

---

## Summary Table

| Quantity | Value | Units |
|----------|-------|-------|
| **Displacements** | | |
| u₁ | 0 | m |
| u₂ | 5.0 × 10⁻³ | m |
| u₃ | 7.5 × 10⁻³ | m |
| | 5.0 | mm |
| | 7.5 | mm |
| **Strains** | | |
| ε₁ | 5.0 × 10⁻³ | (dimensionless) |
| ε₂ | 2.5 × 10⁻³ | (dimensionless) |
| **Stresses** | | |
| σ₁ | 1000 | MPa |
| σ₂ | 500 | MPa |
| **Internal Forces** | | |
| N₁ | 100 | kN |
| N₂ | 100 | kN |
| **Reactions** | | |
| R₁ | -100 | kN |

---

## Physical Interpretation

1. **Load Distribution**: Both elements carry the same internal force (100 kN) because they're in series. This force flows from node 3 through node 2 to the fixed support at node 1.

2. **Displacement Gradient**: 
   - Element 1 contributes: Δu = 5.0 mm
   - Element 2 contributes: Δu = 2.5 mm
   - Total: 7.5 mm

3. **Stress Relationship**:
   - Element 1: σ₁ = 1000 MPa (higher stress due to smaller area)
   - Element 2: σ₂ = 500 MPa (lower stress due to larger area)
   - Both carry same force but different stresses (A₂ = 2×A₁)

4. **Strain Relationship**:
   - ε₁/ε₂ = 2 (higher strain in smaller element for same load)

5. **Reaction Force**: 100 kN support reaction balances the 100 kN applied load, confirming equilibrium.

---

## Verification Against Analytical Solution

**For Serial Bar Elements**:
```
Total displacement = P/(E×A₁)×L₁ + P/(E×A₂)×L₂

= 100×10³ / (200×10⁹ × 100×10⁻⁶) × 1 + 100×10³ / (200×10⁹ × 200×10⁻⁶) × 1

= 100×10³ / (200×10³) + 100×10³ / (400×10³)

= 0.5×10⁻³ + 0.25×10⁻³

= 0.005 + 0.0025 = 0.0075 m = 7.5 mm ✓
```

**FEM matches analytical solution exactly!**

---

## Key Lessons

✓ **Assembly Rule**: Element stiffness contributions add at shared nodes  
✓ **Boundary Conditions**: Essential BCs reduce system size  
✓ **Load Path**: Series elements experience same internal force  
✓ **Stress vs. Strain**: Different for same force on different areas  
✓ **Equilibrium**: Always verify force balance  
✓ **Verification**: Compare with analytical solutions when possible  

---

**Continue to practice → [02_Solutions.md](./02_Solutions.md) for more complex problems**
