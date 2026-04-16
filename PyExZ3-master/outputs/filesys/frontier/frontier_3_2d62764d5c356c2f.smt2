(set-logic ALL)
; Frontier Constraint ID: 2d62764d5c356c2f
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1015)) (False)
(assert (not (= x 1015)))

; Query: ((== x 1016)) (False)
(assert (not (not (= x 1016))))

(check-sat)
(get-model)
