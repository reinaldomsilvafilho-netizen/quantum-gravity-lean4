import Lake
open Lake DSL

package «YangMills» where

lean_lib «YangMills» where

@[default_target]
lean_exe «yang_mills_proofs» where
  root := `Main
