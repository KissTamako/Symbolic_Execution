(set-logic ALL)
; Constraint ID: b94d77dfc65a99bd
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59641)) (False)
(assert (not (not (= x 59641))))

(check-sat)
(get-model)
