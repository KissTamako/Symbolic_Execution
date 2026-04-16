(set-logic ALL)
; Constraint ID: a4fb7b637a13737c
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59689)) (False)
(assert (not (= x 59689)))

; Query: ((== x 59690)) (False)
(assert (not (not (= x 59690))))

(check-sat)
(get-model)
