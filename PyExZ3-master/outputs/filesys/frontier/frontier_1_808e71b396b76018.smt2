(set-logic ALL)
; Frontier Constraint ID: 808e71b396b76018
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2812)) (False)
(assert (not (= x 2812)))

; Query: ((== x 2813)) (False)
(assert (not (not (= x 2813))))

(check-sat)
(get-model)
