(set-logic ALL)
; Frontier Constraint ID: ee98000af9180300
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1723)) (False)
(assert (not (not (= x 1723))))

(check-sat)
(get-model)
