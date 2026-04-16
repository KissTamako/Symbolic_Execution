(set-logic ALL)
; Constraint ID: edc9f67646903190
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59476)) (False)
(assert (not (not (= x 59476))))

(check-sat)
(get-model)
