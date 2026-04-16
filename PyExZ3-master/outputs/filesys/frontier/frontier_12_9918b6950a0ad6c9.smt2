(set-logic ALL)
; Frontier Constraint ID: 9918b6950a0ad6c9
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2530)) (False)
(assert (not (not (= x 2530))))

(check-sat)
(get-model)
