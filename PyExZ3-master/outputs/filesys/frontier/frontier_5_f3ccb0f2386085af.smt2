(set-logic ALL)
; Frontier Constraint ID: f3ccb0f2386085af
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2518)) (False)
(assert (not (= x 2518)))

; Query: ((== x 2519)) (False)
(assert (not (not (= x 2519))))

(check-sat)
(get-model)
