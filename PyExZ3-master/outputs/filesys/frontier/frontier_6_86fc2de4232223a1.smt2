(set-logic ALL)
; Frontier Constraint ID: 86fc2de4232223a1
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1471)) (False)
(assert (not (not (= x 1471))))

(check-sat)
(get-model)
