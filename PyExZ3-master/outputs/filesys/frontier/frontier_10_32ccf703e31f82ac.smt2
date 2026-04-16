(set-logic ALL)
; Constraint ID: 32ccf703e31f82ac
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59626)) (False)
(assert (not (not (= x 59626))))

(check-sat)
(get-model)
