(set-logic ALL)
; Frontier Constraint ID: 615fde7957540115
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 673)) (False)
(assert (not (not (= x 673))))

(check-sat)
(get-model)
