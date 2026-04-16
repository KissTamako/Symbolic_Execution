(set-logic ALL)
; Constraint ID: 9a5f9b5e7f457dc3
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60676)) (False)
(assert (not (not (= x 60676))))

(check-sat)
(get-model)
