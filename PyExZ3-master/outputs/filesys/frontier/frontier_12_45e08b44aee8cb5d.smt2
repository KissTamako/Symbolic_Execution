(set-logic ALL)
; Frontier Constraint ID: 45e08b44aee8cb5d
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1030)) (False)
(assert (not (not (= x 1030))))

(check-sat)
(get-model)
