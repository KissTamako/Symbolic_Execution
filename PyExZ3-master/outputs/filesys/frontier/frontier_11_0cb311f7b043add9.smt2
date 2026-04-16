(set-logic ALL)
; Frontier Constraint ID: 0cb311f7b043add9
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1627)) (False)
(assert (not (= x 1627)))

; Query: ((== x 1628)) (False)
(assert (not (not (= x 1628))))

(check-sat)
(get-model)
