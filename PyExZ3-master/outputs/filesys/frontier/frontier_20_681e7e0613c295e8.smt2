(set-logic ALL)
; Constraint ID: 681e7e0613c295e8
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59716)) (False)
(assert (not (not (= x 59716))))

(check-sat)
(get-model)
