(set-logic ALL)
; Frontier Constraint ID: 98c47b2d93101333
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2443)) (False)
(assert (not (not (= x 2443))))

(check-sat)
(get-model)
