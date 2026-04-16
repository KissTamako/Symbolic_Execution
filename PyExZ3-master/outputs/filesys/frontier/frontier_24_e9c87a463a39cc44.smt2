(set-logic ALL)
; Frontier Constraint ID: e9c87a463a39cc44
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 748)) (False)
(assert (not (not (= x 748))))

(check-sat)
(get-model)
