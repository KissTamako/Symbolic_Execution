(set-logic ALL)
; Frontier Constraint ID: 9bdd697bcff005ec
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 358)) (False)
(assert (not (not (= x 358))))

(check-sat)
(get-model)
