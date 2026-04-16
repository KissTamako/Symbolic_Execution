(set-logic ALL)
; Constraint ID: ab7880b41c7e2d46
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60535)) (False)
(assert (not (not (= x 60535))))

(check-sat)
(get-model)
