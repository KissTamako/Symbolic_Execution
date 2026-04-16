(set-logic ALL)
; Frontier Constraint ID: 409fd34ca0a2863f
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 439)) (False)
(assert (not (= x 439)))

; Query: ((== x 440)) (False)
(assert (not (not (= x 440))))

(check-sat)
(get-model)
