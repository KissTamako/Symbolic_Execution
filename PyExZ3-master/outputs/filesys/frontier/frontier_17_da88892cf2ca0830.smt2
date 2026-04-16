(set-logic ALL)
; Frontier Constraint ID: da88892cf2ca0830
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 436)) (False)
(assert (not (= x 436)))

; Query: ((== x 437)) (False)
(assert (not (not (= x 437))))

(check-sat)
(get-model)
