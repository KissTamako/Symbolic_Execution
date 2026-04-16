(set-logic ALL)
; Frontier Constraint ID: 271d69fe7a42c6df
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 355)) (False)
(assert (not (not (= x 355))))

(check-sat)
(get-model)
