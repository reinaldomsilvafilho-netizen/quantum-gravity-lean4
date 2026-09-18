import Lake
open Lake DSL

package «YangMillsMassGap» where

lean_lib «YangMills» where

@[default_target]
lean_exe «ym_proofs» where
  root := `Main
