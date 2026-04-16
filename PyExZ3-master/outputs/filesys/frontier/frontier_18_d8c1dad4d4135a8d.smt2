(set-logic ALL)
; Constraint ID: d8c1dad4d4135a8d
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59413)) (False)
(assert (not (not (= x 59413))))

(check-sat)
(get-model)
