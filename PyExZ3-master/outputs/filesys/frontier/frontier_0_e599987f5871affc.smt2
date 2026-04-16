(set-logic ALL)
; Frontier Constraint ID: e599987f5871affc
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 412)) (False)
(assert (not (not (= x 412))))

(check-sat)
(get-model)
