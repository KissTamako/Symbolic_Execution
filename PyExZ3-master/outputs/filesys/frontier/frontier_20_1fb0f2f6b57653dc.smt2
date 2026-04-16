(set-logic ALL)
; Constraint ID: 1fb0f2f6b57653dc
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59491)) (False)
(assert (not (not (= x 59491))))

(check-sat)
(get-model)
