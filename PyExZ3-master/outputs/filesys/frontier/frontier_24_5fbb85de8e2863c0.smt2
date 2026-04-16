(set-logic ALL)
; Frontier Constraint ID: 5fbb85de8e2863c0
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 448)) (False)
(assert (not (not (= x 448))))

(check-sat)
(get-model)
