(set-logic ALL)
; Frontier Constraint ID: 7463d127a1ebc731
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 712)) (False)
(assert (not (not (= x 712))))

(check-sat)
(get-model)
