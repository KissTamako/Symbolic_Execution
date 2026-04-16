(set-logic ALL)
; Constraint ID: 9f91540b3a3d07e7
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59254)) (False)
(assert (not (not (= x 59254))))

(check-sat)
(get-model)
