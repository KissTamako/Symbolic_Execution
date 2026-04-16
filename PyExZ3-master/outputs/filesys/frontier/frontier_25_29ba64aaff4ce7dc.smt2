(set-logic ALL)
; Frontier Constraint ID: 29ba64aaff4ce7dc
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1723)) (False)
(assert (not (= x 1723)))

; Query: ((== x 1724)) (False)
(assert (not (not (= x 1724))))

(check-sat)
(get-model)
