(set-logic ALL)
; Frontier Constraint ID: 37975680dc280646
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 436)) (False)
(assert (not (not (= x 436))))

(check-sat)
(get-model)
