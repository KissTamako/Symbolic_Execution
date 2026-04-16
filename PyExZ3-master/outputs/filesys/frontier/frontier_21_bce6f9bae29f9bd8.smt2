(set-logic ALL)
; Frontier Constraint ID: bce6f9bae29f9bd8
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2842)) (False)
(assert (not (= x 2842)))

; Query: ((== x 2843)) (False)
(assert (not (not (= x 2843))))

(check-sat)
(get-model)
