(set-logic ALL)
; Frontier Constraint ID: c85e4bbc61269534
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2536)) (False)
(assert (not (not (= x 2536))))

(check-sat)
(get-model)
