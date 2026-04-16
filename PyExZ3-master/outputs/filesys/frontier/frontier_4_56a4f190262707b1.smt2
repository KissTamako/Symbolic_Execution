(set-logic ALL)
; Constraint ID: 56a4f190262707b1
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59242)) (False)
(assert (not (not (= x 59242))))

(check-sat)
(get-model)
