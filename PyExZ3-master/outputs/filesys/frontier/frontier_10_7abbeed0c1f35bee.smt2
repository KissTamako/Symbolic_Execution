(set-logic ALL)
; Constraint ID: 7abbeed0c1f35bee
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60526)) (False)
(assert (not (not (= x 60526))))

(check-sat)
(get-model)
