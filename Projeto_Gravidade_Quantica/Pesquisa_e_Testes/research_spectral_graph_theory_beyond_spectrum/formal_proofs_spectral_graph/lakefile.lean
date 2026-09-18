import Lake
open Lake DSL

package «SpectralGraphBeyondSpectrum» where

lean_lib «SpectralGraph» where

@[default_target]
lean_exe «verify_spectral_graph» where
  root := `Main
