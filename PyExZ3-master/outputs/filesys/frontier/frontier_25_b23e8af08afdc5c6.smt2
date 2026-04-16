(set-logic ALL)
; Frontier Constraint ID: b23e8af08afdc5c6
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 898)) (False)
(assert (not (= x 898)))

; Query: ((== x 899)) (False)
(assert (not (not (= x 899))))

(check-sat)
(get-model)
