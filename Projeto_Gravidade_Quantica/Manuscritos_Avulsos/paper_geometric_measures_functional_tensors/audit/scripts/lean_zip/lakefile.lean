import Lake
open Lake DSL

package «BeyondTheSpectrum» where

lean_lib «BTS» where

@[default_target]
lean_exe «bts» where
  root := `Main
