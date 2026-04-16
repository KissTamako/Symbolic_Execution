(set-logic ALL)
; Frontier Constraint ID: f10d2d21c6f18f96
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 862)) (False)
(assert (not (not (= x 862))))

(check-sat)
(get-model)
