(set-logic ALL)
; Frontier Constraint ID: f9648b6f96d22143
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1495)) (False)
(assert (not (= x 1495)))

; Query: ((== x 1496)) (False)
(assert (not (not (= x 1496))))

(check-sat)
(get-model)
