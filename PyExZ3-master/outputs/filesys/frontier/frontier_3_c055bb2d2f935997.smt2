(set-logic ALL)
; Frontier Constraint ID: c055bb2d2f935997
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1840)) (False)
(assert (not (= x 1840)))

; Query: ((== x 1841)) (False)
(assert (not (not (= x 1841))))

(check-sat)
(get-model)
