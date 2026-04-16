(set-logic ALL)
; Constraint ID: d69c301a79fa7524
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60286)) (False)
(assert (not (not (= x 60286))))

(check-sat)
(get-model)
