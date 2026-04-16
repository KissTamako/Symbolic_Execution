(set-logic ALL)
; Constraint ID: 2443e63f9447f1c9
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59923)) (False)
(assert (not (not (= x 59923))))

(check-sat)
(get-model)
