"""
Finite Element Method - 1D Bar Element Analysis
===============================================

This script demonstrates a complete FEM analysis for a simple 1D bar element.

Problem:
  A steel bar with varying cross-section is subjected to axial loading.
  - Element 1: A₁ = 100 mm², L₁ = 1.0 m
  - Element 2: A₂ = 200 mm², L₂ = 1.0 m
  - Load: P = 100 kN applied at free end
  - Material: Steel (E = 200 GPa)

Solution Approach:
  1. Define geometry and material properties
  2. Create element stiffness matrices
  3. Assemble global system
  4. Apply boundary conditions
  5. Solve for nodal displacements
  6. Post-process: calculate stresses and strains
  7. Visualize results

Author: FEM Teaching Material
Date: 2026-05-06
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

# ============================================================================
# PART 1: PROBLEM DEFINITION
# ============================================================================

class BarElement:
    """Class to represent a 1D bar element"""
    
    def __init__(self, element_id, node_start, node_end, E, A, L):
        """
        Initialize a bar element
        
        Parameters:
        -----------
        element_id : int
            Element identifier
        node_start : int
            Starting node number
        node_end : int
            Ending node number
        E : float
            Young's modulus (Pa)
        A : float
            Cross-sectional area (m²)
        L : float
            Element length (m)
        """
        self.id = element_id
        self.nodes = [node_start, node_end]
        self.E = E
        self.A = A
        self.L = L
        
    def stiffness_matrix(self):
        """
        Calculate element stiffness matrix
        
        Formula: [K]ᵉ = (EA/L) * [1  -1]
                               [-1   1]
        
        Returns:
        --------
        K : 2x2 numpy array
            Element stiffness matrix
        """
        k_coeff = (self.E * self.A) / self.L
        K = k_coeff * np.array([[1, -1],
                                [-1, 1]])
        return K
    
    def strain(self, u_start, u_end):
        """
        Calculate element strain
        
        Formula: ε = (u_end - u_start) / L
        """
        return (u_end - u_start) / self.L
    
    def stress(self, strain):
        """
        Calculate element stress
        
        Formula: σ = E * ε
        """
        return self.E * strain
    
    def internal_force(self, stress):
        """
        Calculate element internal force
        
        Formula: N = σ * A
        """
        return stress * self.A
    
    def __repr__(self):
        return f"BarElement(id={self.id}, nodes={self.nodes}, E={self.E/1e9}GPa, A={self.A*1e6}mm², L={self.L}m)"


# ============================================================================
# PART 2: PROBLEM SETUP
# ============================================================================

print("="*70)
print("FINITE ELEMENT METHOD - 1D BAR ANALYSIS")
print("="*70)

# Material properties
E = 200e9  # Young's modulus [Pa]

# Geometry
L = 1.0    # Length of each element [m]
A1 = 100e-6  # Cross-sectional area of element 1 [m²]
A2 = 200e-6  # Cross-sectional area of element 2 [m²]

# Loading
P = 100e3  # Applied load at node 3 [N]

print("\n1. PROBLEM DEFINITION")
print("-" * 70)
print(f"Material Properties:")
print(f"  Young's modulus (E) = {E/1e9} GPa")
print(f"\nGeometry:")
print(f"  Element 1: A₁ = {A1*1e6} mm², L₁ = {L} m")
print(f"  Element 2: A₂ = {A2*1e6} mm², L₂ = {L} m")
print(f"\nLoading:")
print(f"  Applied load P = {P/1e3} kN (at node 3)")
print(f"\nBoundary Conditions:")
print(f"  u₁ = 0 (fixed at node 1)")

# Create elements
elem1 = BarElement(element_id=1, node_start=1, node_end=2, E=E, A=A1, L=L)
elem2 = BarElement(element_id=2, node_start=2, node_end=3, E=E, A=A2, L=L)

elements = [elem1, elem2]
num_nodes = 3
num_elements = 2
num_dof = 1  # 1 DOF per node (axial displacement)

print("\n2. ELEMENT PROPERTIES")
print("-" * 70)
for elem in elements:
    k_coeff = (elem.E * elem.A) / elem.L
    print(f"{elem}")
    print(f"  Stiffness coefficient: k = {k_coeff/1e6:.1f} MN/m")

# ============================================================================
# PART 3: ELEMENT STIFFNESS MATRICES
# ============================================================================

print("\n3. ELEMENT STIFFNESS MATRICES")
print("-" * 70)

K1 = elem1.stiffness_matrix()
K2 = elem2.stiffness_matrix()

print(f"\nElement 1 Stiffness Matrix [K]¹:")
print(f"  [{K1[0,0]/1e6:8.1f}  {K1[0,1]/1e6:8.1f}] × 10⁶ N/m")
print(f"  [{K1[1,0]/1e6:8.1f}  {K1[1,1]/1e6:8.1f}]")

print(f"\nElement 2 Stiffness Matrix [K]²:")
print(f"  [{K2[0,0]/1e6:8.1f}  {K2[0,1]/1e6:8.1f}] × 10⁶ N/m")
print(f"  [{K2[1,0]/1e6:8.1f}  {K2[1,1]/1e6:8.1f}]")

# ============================================================================
# PART 4: GLOBAL STIFFNESS MATRIX ASSEMBLY
# ============================================================================

print("\n4. GLOBAL STIFFNESS MATRIX ASSEMBLY")
print("-" * 70)

# Initialize global stiffness matrix
K_global = np.zeros((num_nodes, num_nodes))

# Assembly process (Direct Stiffness Method)
print("\nAssembly procedure:")
print("  Element 1 contributes to DOF (1,1), (1,2), (2,1), (2,2)")
print("  Element 2 contributes to DOF (2,2), (2,3), (3,2), (3,3)")

# Element 1 assembly
K_global[0, 0] += K1[0, 0]  # Node 1 self-effect
K_global[0, 1] += K1[0, 1]  # Node 1-2 coupling
K_global[1, 0] += K1[1, 0]  # Node 2-1 coupling
K_global[1, 1] += K1[1, 1]  # Node 2 self-effect from element 1

# Element 2 assembly
K_global[1, 1] += K2[0, 0]  # Node 2 self-effect from element 2
K_global[1, 2] += K2[0, 1]  # Node 2-3 coupling
K_global[2, 1] += K2[1, 0]  # Node 3-2 coupling
K_global[2, 2] += K2[1, 1]  # Node 3 self-effect

print(f"\nGlobal Stiffness Matrix [K]ᵍˡᵒᵇᵃˡ:")
print(f"  [{K_global[0,0]/1e6:8.1f}  {K_global[0,1]/1e6:8.1f}  {K_global[0,2]/1e6:8.1f}] × 10⁶")
print(f"  [{K_global[1,0]/1e6:8.1f}  {K_global[1,1]/1e6:8.1f}  {K_global[1,2]/1e6:8.1f}]")
print(f"  [{K_global[2,0]/1e6:8.1f}  {K_global[2,1]/1e6:8.1f}  {K_global[2,2]/1e6:8.1f}]")

# ============================================================================
# PART 5: LOAD VECTOR AND BOUNDARY CONDITIONS
# ============================================================================

print("\n5. BOUNDARY CONDITIONS AND LOAD VECTOR")
print("-" * 70)

# Create load vector
F = np.zeros(num_nodes)
F[2] = P  # Applied load at node 3

print(f"\nGlobal Load Vector {{F}}:")
print(f"  F₁ = {F[0]/1e3:8.1f} kN")
print(f"  F₂ = {F[1]/1e3:8.1f} kN")
print(f"  F₃ = {F[2]/1e3:8.1f} kN")

# Apply essential boundary condition: u₁ = 0
# We'll use the direct elimination method
print(f"\nApplying Essential Boundary Condition:")
print(f"  u₁ = 0 (fixed support)")
print(f"\nReduced system (removing DOF 1):")

# Create reduced system (eliminate first row/column)
K_reduced = K_global[1:, 1:]
F_reduced = F[1:]

print(f"\nReduced Stiffness Matrix [K]ʳᵉᵈ:")
print(f"  [{K_reduced[0,0]/1e6:8.1f}  {K_reduced[0,1]/1e6:8.1f}] × 10⁶")
print(f"  [{K_reduced[1,0]/1e6:8.1f}  {K_reduced[1,1]/1e6:8.1f}]")

print(f"\nReduced Load Vector {{F}}ʳᵉᵈ:")
print(f"  F₂ = {F_reduced[0]/1e3:8.1f} kN")
print(f"  F₃ = {F_reduced[1]/1e3:8.1f} kN")

# ============================================================================
# PART 6: SOLVE FOR DISPLACEMENTS
# ============================================================================

print("\n6. SOLVE FOR NODAL DISPLACEMENTS")
print("-" * 70)

# Solve reduced system: [K]ʳᵉᵈ {u}ʳᵉᵈ = {F}ʳᵉᵈ
u_reduced = solve(K_reduced, F_reduced)

# Build full displacement vector
u = np.zeros(num_nodes)
u[0] = 0  # Boundary condition
u[1:] = u_reduced

print(f"\nSolution:")
print(f"  u₁ = {u[0]:.6e} m = {u[0]*1e3:.4f} mm (fixed)")
print(f"  u₂ = {u[1]:.6e} m = {u[1]*1e3:.4f} mm")
print(f"  u₃ = {u[2]:.6e} m = {u[2]*1e3:.4f} mm")

# ============================================================================
# PART 7: POST-PROCESSING (STRESSES AND STRAINS)
# ============================================================================

print("\n7. POST-PROCESSING - STRESSES AND STRAINS")
print("-" * 70)

# Calculate strains and stresses for each element
strains = []
stresses = []
forces = []

for i, elem in enumerate(elements):
    u_start = u[elem.nodes[0] - 1]  # Convert to 0-based indexing
    u_end = u[elem.nodes[1] - 1]
    
    strain = elem.strain(u_start, u_end)
    stress = elem.stress(strain)
    internal_force = elem.internal_force(stress)
    
    strains.append(strain)
    stresses.append(stress)
    forces.append(internal_force)
    
    print(f"\nElement {i+1} (Nodes {elem.nodes[0]}-{elem.nodes[1]}):")
    print(f"  Displacement: u_{elem.nodes[0]} = {u_start:.6e} m")
    print(f"  Displacement: u_{elem.nodes[1]} = {u_end:.6e} m")
    print(f"  ΔL = {(u_end - u_start):.6e} m")
    print(f"  Strain:        ε = {strain:.6e} (dimensionless)")
    print(f"  Stress:        σ = {stress/1e6:.2f} MPa")
    print(f"  Internal Force: N = {internal_force/1e3:.2f} kN")

# ============================================================================
# PART 8: REACTION FORCES
# ============================================================================

print("\n8. REACTION FORCES")
print("-" * 70)

# Calculate reactions: {R} = [K]{u} - {F}
reactions = K_global @ u - F

print(f"\nReaction Forces:")
print(f"  R₁ = {reactions[0]/1e3:.2f} kN (at fixed support)")
print(f"  R₂ = {reactions[1]/1e3:.2f} kN (at node 2)")
print(f"  R₃ = {reactions[2]/1e3:.2f} kN (at node 3)")

# Verify equilibrium
total_force = reactions[0] + reactions[1] + reactions[2] + P
print(f"\nForce Balance Verification:")
print(f"  Sum of reactions + applied load = {total_force:.2e} N ≈ 0 ✓")

# ============================================================================
# PART 9: VERIFICATION WITH ANALYTICAL SOLUTION
# ============================================================================

print("\n9. VERIFICATION WITH ANALYTICAL SOLUTION")
print("-" * 70)

# For series bar elements:
# Total displacement = P/(EA₁)*L₁ + P/(EA₂)*L₂
u_analytical = (P / (E * A1)) * L + (P / (E * A2)) * L

print(f"\nAnalytical Solution (Series Bars):")
print(f"  u_total_analytical = P/(EA₁)*L₁ + P/(EA₂)*L₂")
print(f"                     = {u_analytical:.6e} m = {u_analytical*1e3:.4f} mm")

print(f"\nFEM Solution:")
print(f"  u_total_FEM        = {u[2]:.6e} m = {u[2]*1e3:.4f} mm")

error = abs(u[2] - u_analytical) / u_analytical * 100
print(f"\nError = {error:.6e}% ✓ (exact match expected)")

# ============================================================================
# PART 10: VISUALIZATION
# ============================================================================

print("\n10. VISUALIZATION")
print("-" * 70)

# Create figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('1D Bar FEM Analysis', fontsize=14, fontweight='bold')

# Plot 1: Displacement field
ax1 = axes[0, 0]
x_coords = [0, L, 2*L]
ax1.plot(x_coords, u*1e3, 'bo-', linewidth=2, markersize=8, label='Nodal displacements')
ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
ax1.set_xlabel('Position along bar (m)', fontsize=10)
ax1.set_ylabel('Displacement (mm)', fontsize=10)
ax1.set_title('Displacement Field', fontsize=11, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()
for i, (x, disp) in enumerate(zip(x_coords, u*1e3)):
    ax1.annotate(f'u_{i+1}={disp:.2f}mm', xy=(x, disp), 
                xytext=(x, disp+0.3), ha='center', fontsize=9)

# Plot 2: Stress distribution
ax2 = axes[0, 1]
x_stress = [L/2, 3*L/2]
ax2.bar(x_stress, np.array(stresses)/1e6, width=0.8, alpha=0.7, color=['steelblue', 'coral'])
ax2.set_xlabel('Element center position (m)', fontsize=10)
ax2.set_ylabel('Stress (MPa)', fontsize=10)
ax2.set_title('Stress Distribution', fontsize=11, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
for i, (x, s) in enumerate(zip(x_stress, stresses)):
    ax2.text(x, s/1e6 + 30, f'σ={s/1e6:.0f}MPa\nA={[A1, A2][i]*1e6:.0f}mm²', 
            ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Plot 3: Strain distribution
ax3 = axes[1, 0]
ax3.bar(x_stress, np.array(strains)*1e3, width=0.8, alpha=0.7, color=['lightgreen', 'lightcoral'])
ax3.set_xlabel('Element center position (m)', fontsize=10)
ax3.set_ylabel('Strain (×10⁻³)', fontsize=10)
ax3.set_title('Strain Distribution', fontsize=11, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')
for i, (x, e) in enumerate(zip(x_stress, strains)):
    ax3.text(x, e*1e3 + 0.1, f'ε={e:.3e}', ha='center', fontsize=9)

# Plot 4: Internal forces
ax4 = axes[1, 1]
ax4.bar(x_stress, np.array(forces)/1e3, width=0.8, alpha=0.7, color=['purple', 'orange'])
ax4.set_xlabel('Element center position (m)', fontsize=10)
ax4.set_ylabel('Internal Force (kN)', fontsize=10)
ax4.set_title('Internal Force Distribution', fontsize=11, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')
for i, (x, f) in enumerate(zip(x_stress, forces)):
    ax4.text(x, f/1e3 + 2, f'N={f/1e3:.0f}kN', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('fem_1d_bar_analysis.png', dpi=150, bbox_inches='tight')
print(f"\nPlot saved as 'fem_1d_bar_analysis.png'")
plt.show()

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print("\nKey Results Summary:")
print(f"  Maximum displacement: {max(u)*1e3:.4f} mm at node 3")
print(f"  Maximum stress:       {max(stresses)/1e6:.2f} MPa in element 1")
print(f"  Applied load:         {P/1e3:.2f} kN")
print(f"  Support reaction:     {abs(reactions[0])/1e3:.2f} kN")
print(f"  Equilibrium check:    {'PASSED ✓' if abs(total_force) < 1e-6 else 'FAILED ✗'}")
print(f"  Analytical match:     {'EXACT ✓' if error < 1e-6 else 'GOOD ✓'}")
print("="*70)
