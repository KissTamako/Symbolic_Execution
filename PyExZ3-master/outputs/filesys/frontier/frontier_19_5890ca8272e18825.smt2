(set-logic ALL)
; Frontier Constraint ID: 5890ca8272e18825
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2839)) (False)
(assert (not (= x 2839)))

; Query: ((== x 2840)) (False)
(assert (not (not (= x 2840))))

(check-sat)
(get-model)
