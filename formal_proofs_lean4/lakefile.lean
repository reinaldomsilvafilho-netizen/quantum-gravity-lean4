import Lake
open Lake DSL

package «QuantumFunctor» where

lean_lib «Category» where
lean_lib «CTensMan» where
lean_lib «Cobordism» where
lean_lib «EmergentFunctor» where
lean_lib «MonoidalCoherence» where
lean_lib «NullEnergy» where

@[default_target]
lean_exe «quantum_functor» where
  root := `Main
