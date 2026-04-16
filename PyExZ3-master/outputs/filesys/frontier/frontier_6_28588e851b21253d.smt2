(set-logic ALL)
; Frontier Constraint ID: 28588e851b21253d
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 346)) (False)
(assert (not (not (= x 346))))

(check-sat)
(get-model)
