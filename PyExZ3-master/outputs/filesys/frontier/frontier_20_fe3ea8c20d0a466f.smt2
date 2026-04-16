(set-logic ALL)
; Frontier Constraint ID: fe3ea8c20d0a466f
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2467)) (False)
(assert (not (not (= x 2467))))

(check-sat)
(get-model)
