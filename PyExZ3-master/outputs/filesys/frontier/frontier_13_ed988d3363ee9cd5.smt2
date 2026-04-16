(set-logic ALL)
; Frontier Constraint ID: ed988d3363ee9cd5
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 655)) (False)
(assert (not (= x 655)))

; Query: ((== x 656)) (False)
(assert (not (not (= x 656))))

(check-sat)
(get-model)
