(set-logic ALL)
; Frontier Constraint ID: e12ad18cf49ba862
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1864)) (False)
(assert (not (not (= x 1864))))

(check-sat)
(get-model)
