(set-logic ALL)
; Frontier Constraint ID: 821664724e968687
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1195)) (False)
(assert (not (not (= x 1195))))

(check-sat)
(get-model)
