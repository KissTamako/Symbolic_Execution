(set-logic ALL)
; Constraint ID: 6654daf42b153ce0
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59419)) (False)
(assert (not (not (= x 59419))))

(check-sat)
(get-model)
