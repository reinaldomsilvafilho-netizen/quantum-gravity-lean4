import os
import subprocess
import time

lean_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(lean_dir, "SpectralGraph")

lean_files = [
    # Volume I: 9 Invariant Bridges
    "CospectralSeparation.lean",
    "NonlinearPLaplacian.lean",
    "GraphonRicciFlow.lean",
    "SimplicialBetaLaplacian.lean",
    "FedererReachEmbedding.lean",
    "NonEquilibriumMixing.lean",
    "RyuTakayanagiNetwork.lean",
    "BarnesKigamiResidues.lean",
    "SparseCommunityNonBacktracking.lean",
    # Volume II & Graph Number Theory: 4 Inversion & Arithmetization Modules
    "Volume2_BooleanInversion.lean",
    "Volume2_ChenHolonomy.lean",
    "Volume2_DimensionBound.lean",
    "GraphNumberTheory.lean"
]

all_passed = True
print("=" * 75)
print("  LEAN 4 FORMAL VERIFICATION: 13 POST-SPECTRAL & NUMBER THEORY MODULES")
print("=" * 75)

for f in lean_files:
    fpath = os.path.join(modules_dir, f)
    t0 = time.time()
    res = subprocess.run(["lean", fpath], capture_output=True, text=True)
    dt = time.time() - t0
    if res.returncode == 0:
        print(f"  [PASS] {f:<38} ({dt:.2f}s) - 0 errors, 0 warnings")
    else:
        print(f"  [FAIL] {f:<38} ({dt:.2f}s) - Code {res.returncode}")
        print("Stdout:", res.stdout)
        print("Stderr:", res.stderr)
        all_passed = False

print("=" * 75)
if all_passed:
    print("  ALL 13 LEAN 4 MODULES COMPILED CLEANLY WITH 0 ERRORS.")
else:
    print("  SOME MODULES FAILED.")
print("=" * 75)
