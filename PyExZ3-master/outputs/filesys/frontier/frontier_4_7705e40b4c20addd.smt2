(set-logic ALL)
; Constraint ID: 7705e40b4c20addd
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59317)) (False)
(assert (not (not (= x 59317))))

(check-sat)
(get-model)
