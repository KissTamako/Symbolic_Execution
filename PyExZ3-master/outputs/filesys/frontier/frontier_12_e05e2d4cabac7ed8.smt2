(set-logic ALL)
; Constraint ID: e05e2d4cabac7ed8
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59554)) (False)
(assert (not (not (= x 59554))))

(check-sat)
(get-model)
