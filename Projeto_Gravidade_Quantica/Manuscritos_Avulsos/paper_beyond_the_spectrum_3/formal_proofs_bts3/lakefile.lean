import Lake
open Lake DSL

package «BeyondTheSpectrum3» where

lean_lib «BTS3» where

@[default_target]
lean_exe «bts3» where
  root := `Main
