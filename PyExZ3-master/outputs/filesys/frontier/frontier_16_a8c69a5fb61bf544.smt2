(set-logic ALL)
; Frontier Constraint ID: a8c69a5fb61bf544
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 736)) (False)
(assert (not (not (= x 736))))

(check-sat)
(get-model)
