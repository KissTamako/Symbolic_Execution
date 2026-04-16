(set-logic ALL)
; Constraint ID: dff0f9925534e87c
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60445)) (False)
(assert (not (not (= x 60445))))

(check-sat)
(get-model)
