(set-logic ALL)
; Constraint ID: 3fe0a0545d5710eb
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59560)) (False)
(assert (not (not (= x 59560))))

(check-sat)
(get-model)
