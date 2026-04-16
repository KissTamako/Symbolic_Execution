(set-logic ALL)
; Frontier Constraint ID: a2e750c4776e4457
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1852)) (False)
(assert (not (not (= x 1852))))

(check-sat)
(get-model)
