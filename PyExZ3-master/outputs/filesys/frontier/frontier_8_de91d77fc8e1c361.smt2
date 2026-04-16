(set-logic ALL)
; Frontier Constraint ID: de91d77fc8e1c361
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1699)) (False)
(assert (not (not (= x 1699))))

(check-sat)
(get-model)
