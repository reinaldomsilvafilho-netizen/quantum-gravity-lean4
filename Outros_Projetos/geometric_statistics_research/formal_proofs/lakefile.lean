import Lake
open Lake DSL

package «GeometricStatistics» where

lean_lib «GeometricStatistics» where

@[default_target]
lean_exe «geom_stat_proofs» where
  root := `Main
