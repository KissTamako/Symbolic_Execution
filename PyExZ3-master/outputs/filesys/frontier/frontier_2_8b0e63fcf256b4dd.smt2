(set-logic ALL)
; Constraint ID: 8b0e63fcf256b4dd
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59689)) (False)
(assert (not (not (= x 59689))))

(check-sat)
(get-model)
