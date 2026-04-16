(set-logic ALL)
; Frontier Constraint ID: 5e8f7f3722aa21f2
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 361)) (False)
(assert (not (not (= x 361))))

(check-sat)
(get-model)
