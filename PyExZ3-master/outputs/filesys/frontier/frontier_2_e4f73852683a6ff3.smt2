(set-logic ALL)
; Frontier Constraint ID: e4f73852683a6ff3
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1465)) (False)
(assert (not (not (= x 1465))))

(check-sat)
(get-model)
