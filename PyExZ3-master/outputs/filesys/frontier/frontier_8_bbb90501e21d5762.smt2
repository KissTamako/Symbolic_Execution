(set-logic ALL)
; Frontier Constraint ID: bbb90501e21d5762
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2524)) (False)
(assert (not (not (= x 2524))))

(check-sat)
(get-model)
