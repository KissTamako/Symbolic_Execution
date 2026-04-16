(set-logic ALL)
; Constraint ID: 25918050d88dd2ae
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59713)) (False)
(assert (not (not (= x 59713))))

(check-sat)
(get-model)
