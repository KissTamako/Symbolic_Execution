(set-logic ALL)
; Constraint ID: 99f45dd6821d1d89
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59692)) (False)
(assert (not (not (= x 59692))))

(check-sat)
(get-model)
