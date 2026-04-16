(set-logic ALL)
; Frontier Constraint ID: d5d13552ba91d717
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1696)) (False)
(assert (not (not (= x 1696))))

(check-sat)
(get-model)
