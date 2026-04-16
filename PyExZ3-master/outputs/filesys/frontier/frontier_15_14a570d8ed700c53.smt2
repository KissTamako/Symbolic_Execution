(set-logic ALL)
; Frontier Constraint ID: 14a570d8ed700c53
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1633)) (False)
(assert (not (= x 1633)))

; Query: ((== x 1634)) (False)
(assert (not (not (= x 1634))))

(check-sat)
(get-model)
