(set-logic ALL)
; Frontier Constraint ID: f14a3664ee4b7322
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2815)) (False)
(assert (not (= x 2815)))

; Query: ((== x 2816)) (False)
(assert (not (not (= x 2816))))

(check-sat)
(get-model)
