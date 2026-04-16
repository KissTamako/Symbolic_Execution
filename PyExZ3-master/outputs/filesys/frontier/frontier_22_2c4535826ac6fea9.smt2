(set-logic ALL)
; Frontier Constraint ID: 2c4535826ac6fea9
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2470)) (False)
(assert (not (not (= x 2470))))

(check-sat)
(get-model)
