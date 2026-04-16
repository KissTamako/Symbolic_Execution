(set-logic ALL)
; Frontier Constraint ID: 089ce2a7aad59a93
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2473)) (False)
(assert (not (not (= x 2473))))

(check-sat)
(get-model)
