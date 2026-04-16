(set-logic ALL)
; Constraint ID: 35991f4b2370e348
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59473)) (False)
(assert (not (not (= x 59473))))

(check-sat)
(get-model)
