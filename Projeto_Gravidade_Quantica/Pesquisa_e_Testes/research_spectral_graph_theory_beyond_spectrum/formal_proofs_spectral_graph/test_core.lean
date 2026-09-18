
-- Test whether Finset or List is standard
def test_sublist (e : List Nat) : Nat := e.length

#eval test_sublist [1, 2, 3]
