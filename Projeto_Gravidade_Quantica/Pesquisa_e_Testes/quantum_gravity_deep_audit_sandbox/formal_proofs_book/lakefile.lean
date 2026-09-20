import Lake
open Lake DSL

package «UnifiedQuantumGravityBook» where

lean_lib «Book» where

@[default_target]
lean_exe «book_proofs» where
  root := `Main
