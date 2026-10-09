#!/usr/bin/env bash
# Checks the LeanReal modules with `lean` directly, without `lake`.
# It reads, read-only, the Mathlib .olean files already built in
# ../formal_proofs_book/.lake/packages (same toolchain and Mathlib revision).
# The .olean files of the LeanReal modules go to .olean_local/ (git-ignored).
#
# Canonical route on a clean machine instead of this script:
#   lake exe cache get && lake build
#
# Usage: ./verificar.sh                    -> the nine LeanReal modules, in dependency order, then LeanReal.lean
#        ARQ=mutants/M1_KK_3para2.lean ./verificar.sh  -> one file (run the modules first)
set -e
here="$(cd "$(dirname "$0")" && pwd)"
pk="$here/../formal_proofs_book/.lake/packages"
mkdir -p "$here/.olean_local/LeanReal"
lp="$(cygpath -m "$here/.olean_local")"
for d in mathlib batteries aesop Qq proofwidgets plausible importGraph LeanSearchClient; do
  lp="$lp;$(cygpath -m "$pk/$d/.lake/build/lib/lean")"
done
export LEAN_PATH="$lp"
lean="${LEAN:-$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc2/bin/lean.exe}"
if [ -n "$ARQ" ]; then echo "== $ARQ"; "$lean" "$ARQ"; exit; fi
for m in Chap03Pascal Chap12Constraint Chap12ConstraintMatrix Falsified Witnesses Fermions YangMills BeyondSpectrum1 FunctorialBridge FunctorialBridge2 FunctorialBridge3 FermionsEuler BeyondSpectrum2Iso Chap02Graphon BeyondSpectrum3_T1 BeyondSpectrum1_B2 BeyondSpectrum1_B4 YangMills_Y5; do
  echo "== $m"; "$lean" "$here/LeanReal/$m.lean" -o "$here/.olean_local/LeanReal/$m.olean"
done
echo "== LeanReal.lean"; "$lean" "$here/LeanReal.lean"
