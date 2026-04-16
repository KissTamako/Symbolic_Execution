(set-logic ALL)
; Frontier Constraint ID: ce9aefbdc4eea108
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 370)) (False)
(assert (not (= x 370)))

; Query: ((== x 371)) (False)
(assert (not (not (= x 371))))

(check-sat)
(get-model)
