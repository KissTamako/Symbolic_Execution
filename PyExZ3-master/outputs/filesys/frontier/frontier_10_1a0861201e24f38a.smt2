(set-logic ALL)
; Frontier Constraint ID: 1a0861201e24f38a
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1177)) (False)
(assert (not (not (= x 1177))))

(check-sat)
(get-model)
