import Lake
open Lake DSL

package «UnconditionalYM» where

lean_lib «UnconditionalYM» where

@[default_target]
lean_exe «unconditional_proofs» where
  root := `Main
