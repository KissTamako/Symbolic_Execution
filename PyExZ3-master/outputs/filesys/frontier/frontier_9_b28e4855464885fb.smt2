(set-logic ALL)
; Frontier Constraint ID: b28e4855464885fb
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2524)) (False)
(assert (not (= x 2524)))

; Query: ((== x 2525)) (False)
(assert (not (not (= x 2525))))

(check-sat)
(get-model)
