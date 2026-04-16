(set-logic ALL)
; Frontier Constraint ID: cb414f16fa7a0f35
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 442)) (False)
(assert (not (= x 442)))

; Query: ((== x 443)) (False)
(assert (not (not (= x 443))))

(check-sat)
(get-model)
