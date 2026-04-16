(set-logic ALL)
; Frontier Constraint ID: 49a92b03113a5553
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 433)) (False)
(assert (not (= x 433)))

; Query: ((== x 434)) (False)
(assert (not (not (= x 434))))

(check-sat)
(get-model)
