(set-logic ALL)
; Frontier Constraint ID: 9815631520f24cc7
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1612)) (False)
(assert (not (= x 1612)))

; Query: ((== x 1613)) (False)
(assert (not (not (= x 1613))))

(check-sat)
(get-model)
