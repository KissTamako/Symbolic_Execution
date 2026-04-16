(set-logic ALL)
; Frontier Constraint ID: 34a696612e1e2ff2
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1699)) (False)
(assert (not (= x 1699)))

; Query: ((== x 1700)) (False)
(assert (not (not (= x 1700))))

(check-sat)
(get-model)
