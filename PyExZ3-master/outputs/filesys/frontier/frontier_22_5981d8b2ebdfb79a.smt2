(set-logic ALL)
; Constraint ID: 5981d8b2ebdfb79a
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59494)) (False)
(assert (not (not (= x 59494))))

(check-sat)
(get-model)
