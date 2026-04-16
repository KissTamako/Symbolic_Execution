(set-logic ALL)
; Constraint ID: 45bd0896d4077496
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59470)) (False)
(assert (not (not (= x 59470))))

(check-sat)
(get-model)
