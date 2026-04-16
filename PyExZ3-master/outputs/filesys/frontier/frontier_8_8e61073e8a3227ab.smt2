(set-logic ALL)
; Frontier Constraint ID: 8e61073e8a3227ab
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 724)) (False)
(assert (not (not (= x 724))))

(check-sat)
(get-model)
