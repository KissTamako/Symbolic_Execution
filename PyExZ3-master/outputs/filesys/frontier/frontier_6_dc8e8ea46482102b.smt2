(set-logic ALL)
; Frontier Constraint ID: dc8e8ea46482102b
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 646)) (False)
(assert (not (not (= x 646))))

(check-sat)
(get-model)
