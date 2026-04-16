(set-logic ALL)
; Frontier Constraint ID: e4984202fa7ee128
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1720)) (False)
(assert (not (not (= x 1720))))

(check-sat)
(get-model)
