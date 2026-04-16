(set-logic ALL)
; Constraint ID: 1af9aef9e3e4d3e8
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59935)) (False)
(assert (not (not (= x 59935))))

(check-sat)
(get-model)
