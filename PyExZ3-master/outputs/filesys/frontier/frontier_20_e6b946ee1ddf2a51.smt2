(set-logic ALL)
; Frontier Constraint ID: e6b946ee1ddf2a51
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2842)) (False)
(assert (not (not (= x 2842))))

(check-sat)
(get-model)
