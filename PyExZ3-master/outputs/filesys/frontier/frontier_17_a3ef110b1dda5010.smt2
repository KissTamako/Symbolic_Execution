(set-logic ALL)
; Frontier Constraint ID: a3ef110b1dda5010
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 736)) (False)
(assert (not (= x 736)))

; Query: ((== x 737)) (False)
(assert (not (not (= x 737))))

(check-sat)
(get-model)
