(set-logic ALL)
; Frontier Constraint ID: 25e26f74811f78d2
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 574)) (False)
(assert (not (not (= x 574))))

(check-sat)
(get-model)
