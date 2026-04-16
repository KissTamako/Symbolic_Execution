(set-logic ALL)
; Frontier Constraint ID: 72ec3f26e2cf3cf1
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1639)) (False)
(assert (not (= x 1639)))

; Query: ((== x 1640)) (False)
(assert (not (not (= x 1640))))

(check-sat)
(get-model)
