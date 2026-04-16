(set-logic ALL)
; Frontier Constraint ID: 4c2e85bb4e600a35
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 643)) (False)
(assert (not (not (= x 643))))

(check-sat)
(get-model)
