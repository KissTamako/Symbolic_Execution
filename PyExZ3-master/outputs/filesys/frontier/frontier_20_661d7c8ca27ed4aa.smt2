(set-logic ALL)
; Frontier Constraint ID: 661d7c8ca27ed4aa
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2542)) (False)
(assert (not (not (= x 2542))))

(check-sat)
(get-model)
