(set-logic ALL)
; Frontier Constraint ID: b74d61a917c84a8a
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 418)) (False)
(assert (not (not (= x 418))))

(check-sat)
(get-model)
