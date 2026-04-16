(set-logic ALL)
; Frontier Constraint ID: 223a1797a98be1f3
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 445)) (False)
(assert (not (not (= x 445))))

(check-sat)
(get-model)
