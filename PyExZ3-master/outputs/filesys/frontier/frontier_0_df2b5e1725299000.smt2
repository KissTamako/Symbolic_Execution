(set-logic ALL)
; Frontier Constraint ID: df2b5e1725299000
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1462)) (False)
(assert (not (not (= x 1462))))

(check-sat)
(get-model)
