(set-logic ALL)
; Frontier Constraint ID: a081b0ef8d4760be
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 424)) (False)
(assert (not (not (= x 424))))

(check-sat)
(get-model)
