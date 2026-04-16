(set-logic ALL)
; Frontier Constraint ID: 00bffed7f3b0dcd3
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2470)) (False)
(assert (not (= x 2470)))

; Query: ((== x 2471)) (False)
(assert (not (not (= x 2471))))

(check-sat)
(get-model)
