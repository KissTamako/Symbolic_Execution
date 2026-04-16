(set-logic ALL)
; Frontier Constraint ID: 754f4f9f0c499731
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1492)) (False)
(assert (not (not (= x 1492))))

(check-sat)
(get-model)
