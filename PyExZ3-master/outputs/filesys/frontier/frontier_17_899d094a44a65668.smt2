(set-logic ALL)
; Frontier Constraint ID: 899d094a44a65668
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 511)) (False)
(assert (not (= x 511)))

; Query: ((== x 512)) (False)
(assert (not (not (= x 512))))

(check-sat)
(get-model)
