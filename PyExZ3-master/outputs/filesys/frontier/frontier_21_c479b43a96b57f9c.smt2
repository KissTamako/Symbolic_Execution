(set-logic ALL)
; Frontier Constraint ID: c479b43a96b57f9c
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2467)) (False)
(assert (not (= x 2467)))

; Query: ((== x 2468)) (False)
(assert (not (not (= x 2468))))

(check-sat)
(get-model)
