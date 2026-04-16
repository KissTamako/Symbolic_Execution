(set-logic ALL)
; Frontier Constraint ID: cbfea31d77c88d07
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1468)) (False)
(assert (not (not (= x 1468))))

(check-sat)
(get-model)
