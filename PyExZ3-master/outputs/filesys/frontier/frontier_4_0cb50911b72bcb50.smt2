(set-logic ALL)
; Frontier Constraint ID: 0cb50911b72bcb50
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 568)) (False)
(assert (not (not (= x 568))))

(check-sat)
(get-model)
