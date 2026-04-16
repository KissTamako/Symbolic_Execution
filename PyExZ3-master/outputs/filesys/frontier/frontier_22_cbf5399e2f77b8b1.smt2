(set-logic ALL)
; Constraint ID: cbf5399e2f77b8b1
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59344)) (False)
(assert (not (not (= x 59344))))

(check-sat)
(get-model)
