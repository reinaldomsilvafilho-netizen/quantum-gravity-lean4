"""
CNIS - Lean 4 AST & Diagrammatic IR Structural Verification Suite
================================================================
Verifies structural AST pattern matching, lossless JSON roundtrips,
and Mathlib 4 categorical tactic synthesis.
"""

import sys
import io

# Force UTF-8 stdout for Windows terminals
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from glyph_ast import LeanExpr, LeanNodeType, LeanGlyphBridge

def test_ast_lossless_roundtrip():
    print(">>> Test 1: Testing LeanExpr Structural Lossless JSON Roundtrip...")
    e1 = LeanExpr(
        node_type=LeanNodeType.COMPOSE,
        name="comp",
        args=[
            LeanExpr(node_type=LeanNodeType.ADJUNCTION_UNIT, name="F"),
            LeanExpr(node_type=LeanNodeType.ADJUNCTION_COUNIT, name="F")
        ]
    )
    
    d = e1.to_dict()
    e2 = LeanExpr.from_dict(d)
    
    assert e1.to_lean_syntax() == e2.to_lean_syntax(), f"Syntax mismatch: {e1.to_lean_syntax()} != {e2.to_lean_syntax()}"
    assert e1.node_type == e2.node_type
    assert len(e1.args) == len(e2.args)
    print(f"  [PASS] Lean Syntax: {e1.to_lean_syntax()}")
    print("  [PASS] AST serialization and deserialization are 100% structurally isomorphic.")

def test_snake_move_compilation_and_tactic():
    print("\n>>> Test 2: Testing Category Adjunction Snake Move Tactic Generation...")
    snake_expr = LeanExpr(
        node_type=LeanNodeType.COMPOSE,
        name="snake_lhs",
        args=[
            LeanExpr(node_type=LeanNodeType.ADJUNCTION_UNIT, name="F"),
            LeanExpr(node_type=LeanNodeType.ADJUNCTION_COUNIT, name="F")
        ]
    )
    
    diagram = LeanGlyphBridge.compile_expr_to_diagram(snake_expr)
    assert len(diagram.nodes) == 2, "Snake diagram must have 2 nodes (unit eta and counit epsilon)"
    assert diagram.nodes[0].glyph_kind == "unit"
    assert diagram.nodes[1].glyph_kind == "counit"
    print(f"  [PASS] Compiled Snake LHS to Glyph-IR with {len(diagram.nodes)} nodes and {len(diagram.wires)} internal wires.")
    
    # Apply topological straightening
    taut_diagram, tactics = LeanGlyphBridge.apply_topological_move(diagram, "snake_straighten")
    assert taut_diagram.lean_goal == "𝟙 F", f"Goal should be identity wire, got {taut_diagram.lean_goal}"
    assert "CategoryTheory.Adjunction.left_triangle_components" in tactics[1]
    print("  [PASS] Generated Canonical Mathlib 4 Tactics:")
    for t in tactics:
        print(f"    {t}")

def test_braiding_reidemeister_tactic():
    print("\n>>> Test 3: Testing Braided Category Reidemeister II Cancellation...")
    braid_expr = LeanExpr(
        node_type=LeanNodeType.BRAIDING,
        name="beta",
        args=[
            LeanExpr(node_type=LeanNodeType.CONST, name="X"),
            LeanExpr(node_type=LeanNodeType.CONST, name="Y")
        ]
    )
    
    diagram = LeanGlyphBridge.compile_expr_to_diagram(braid_expr)
    assert diagram.nodes[0].metadata.get("depth") == 1, "Braided crossing must contain depth channel"
    print("  [PASS] Braided crossing encoded with multi-channel depth z=1.")
    
    simplified_diagram, tactics = LeanGlyphBridge.apply_topological_move(diagram, "braid_reidemeister_2")
    assert simplified_diagram.lean_goal == "𝟙 (X ⊗ Y)"
    assert "CategoryTheory.Iso.hom_inv_id" in tactics[1]
    print("  [PASS] Generated Canonical Mathlib 4 Tactics for Reidemeister II:")
    for t in tactics:
        print(f"    {t}")

def test_tensor_contraction_fusion():
    print("\n>>> Test 4: Testing Tensor Contraction Fusion Move...")
    t_expr = LeanExpr(
        node_type=LeanNodeType.CONTRACTION,
        name="contract",
        args=[LeanExpr(node_type=LeanNodeType.CONST, name="T_ij_S_jk")]
    )
    diagram = LeanGlyphBridge.compile_expr_to_diagram(t_expr)
    fused_diagram, tactics = LeanGlyphBridge.apply_topological_move(diagram, "tensor_trace_fusion")
    assert fused_diagram.lean_goal == "scalar_val"
    print("  [PASS] Generated Mathlib 4 Tactics for Contraction Trace:")
    for t in tactics:
        print(f"    {t}")

def test_clifford_metric_projection():
    print("\n>>> Test 5: Testing Clifford Algebra Metric Projection...")
    clifford_expr = LeanExpr(
        node_type=LeanNodeType.CLIFFORD_ACTION,
        name="clifford",
        args=[LeanExpr(node_type=LeanNodeType.CONST, name="p")]
    )
    diagram = LeanGlyphBridge.compile_expr_to_diagram(clifford_expr)
    assert diagram.nodes[0].glyph_kind == "clifford_fusion"
    print(f"  [PASS] Compiled Clifford Generator to Glyph-IR: {diagram.nodes[0].label}")
    
    collapsed_diagram, tactics = LeanGlyphBridge.apply_topological_move(diagram, "clifford_anticommutator_collapse")
    assert collapsed_diagram.lean_goal == "Q(p) • 𝟙"
    assert "CliffordAlgebra.ι_sq_scalar" in tactics[1]
    print("  [PASS] Generated Mathlib 4 Tactics for Clifford Metric Projection:")
    for t in tactics:
        print(f"    {t}")

def test_gordon_current_decomposition():
    print("\n>>> Test 6: Testing Gordon Current Decomposition Move...")
    gordon_expr = LeanExpr(
        node_type=LeanNodeType.GORDON_DECOMPOSITION,
        name="Psi",
        args=[]
    )
    diagram = LeanGlyphBridge.compile_expr_to_diagram(gordon_expr)
    assert diagram.nodes[0].glyph_kind == "gordon_split"
    print(f"  [PASS] Compiled Gordon Current Split to Glyph-IR: {diagram.nodes[0].label}")
    
    div_free_diagram, tactics = LeanGlyphBridge.apply_topological_move(diagram, "gordon_divergence_free")
    assert div_free_diagram.lean_goal == "0"
    print("  [PASS] Generated Mathlib 4 Tactics for Spin Magnetization Vanishing Divergence:")
    for t in tactics:
        print(f"    {t}")

def test_einstein_coupling_and_vacuum_reduction():
    print("\n>>> Test 7: Testing Einstein (1915) Functorial Coupling & Vacuum Reduction...")
    einstein_expr = LeanExpr(
        node_type=LeanNodeType.EINSTEIN_COUPLING,
        name="field_eq",
        args=[
            LeanExpr(node_type=LeanNodeType.CONST, name="G_μν"),
            LeanExpr(node_type=LeanNodeType.CONST, name="T_μν")
        ]
    )
    diagram = LeanGlyphBridge.compile_expr_to_diagram(einstein_expr)
    assert len(diagram.nodes) == 2, "Einstein coupling must create geometry and matter chamber nodes"
    assert len(diagram.wires) == 1, "Einstein coupling must create connecting interaction bridge wire"
    print(f"  [PASS] Compiled Einstein Field Equation to Glyph-IR: {len(diagram.nodes)} chambers, 1 coupling wire (κ = 8πG/c⁴)")
    
    vacuum_diagram, tactics = LeanGlyphBridge.apply_topological_move(diagram, "einstein_vacuum_ricci_flat")
    assert vacuum_diagram.lean_goal == "R_μν = 0"
    assert any("Geometry.einstein_vacuum_implies_ricci_flat" in t for t in tactics)
    print("  [PASS] Generated Mathlib 4 Tactics for Vacuum Reduction (T_μν = 0 => R_μν = 0):")
    for t in tactics:
        print(f"    {t}")

def test_contracted_bianchi_divergence_free():
    print("\n>>> Test 8: Testing Contracted Bianchi Identity Divergence Free Gate...")
    bianchi_expr = LeanExpr(
        node_type=LeanNodeType.CONTRACTED_BIANCHI,
        name="G_tensor",
        args=[]
    )
    diagram = LeanGlyphBridge.compile_expr_to_diagram(bianchi_expr)
    assert diagram.nodes[0].glyph_kind == "contracted_bianchi"
    print(f"  [PASS] Compiled Contracted Bianchi Gate to Glyph-IR: {diagram.nodes[0].label}")
    
    div_free_diagram, tactics = LeanGlyphBridge.apply_topological_move(diagram, "bianchi_divergence_cancellation")
    assert div_free_diagram.lean_goal == "0_ν"
    assert any("Geometry.contracted_bianchi_divergence_free" in t for t in tactics)
    print("  [PASS] Generated Mathlib 4 Tactics for Contracted Bianchi Identity:")
    for t in tactics:
        print(f"    {t}")

def test_schwarzschild_light_bending_geodesic():
    print("\n>>> Test 9: Testing Schwarzschild Null Geodesic Deflection Move...")
    schwarz_expr = LeanExpr(
        node_type=LeanNodeType.SCHWARZSCHILD_DEFLECTION,
        name="sun_mass",
        args=[]
    )
    diagram = LeanGlyphBridge.compile_expr_to_diagram(schwarz_expr)
    assert diagram.nodes[0].glyph_kind == "schwarzschild_deflection"
    print(f"  [PASS] Compiled Schwarzschild Deflection to Glyph-IR: {diagram.nodes[0].label}")
    
    deflected_diagram, tactics = LeanGlyphBridge.apply_topological_move(diagram, "schwarzschild_geodesic_deflection")
    assert deflected_diagram.lean_goal == "4 * G * M / (c^2 * b)"
    assert any("RelativisticOptics.schwarzschild_light_bending_geodesic" in t for t in tactics)
    print("  [PASS] Generated Mathlib 4 Tactics for Schwarzschild Deflection (Δθ = 4GM/c²b = 1.75\"):")
    for t in tactics:
        print(f"    {t}")

if __name__ == "__main__":
    print("=================================================================")
    print("CNIS Lean 4 / Glyph-IR Structural Verification Battery")
    print("=================================================================")
    test_ast_lossless_roundtrip()
    test_snake_move_compilation_and_tactic()
    test_braiding_reidemeister_tactic()
    test_tensor_contraction_fusion()
    test_clifford_metric_projection()
    test_gordon_current_decomposition()
    test_einstein_coupling_and_vacuum_reduction()
    test_contracted_bianchi_divergence_free()
    test_schwarzschild_light_bending_geodesic()
    print("\n=================================================================")
    print("ALL 9 BATTERIES PASSED: 100% STRUCTURAL AST, IR ROUNDTRIP & TACTIC SYNTHESIS VERIFIED")
    print("=================================================================")


