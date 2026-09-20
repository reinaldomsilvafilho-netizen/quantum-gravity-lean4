import Lake
open Lake DSL

package «GeometricInference» where

lean_lib «GeometricInference» where

@[default_target]
lean_exe «geometric_inference» where
  root := `Main
