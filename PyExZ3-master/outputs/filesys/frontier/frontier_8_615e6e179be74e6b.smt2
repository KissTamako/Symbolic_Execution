(set-logic ALL)
; Constraint ID: 615e6e179be74e6b
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59998)) (False)
(assert (not (not (= x 59998))))

(check-sat)
(get-model)
