(set-logic ALL)
; Frontier Constraint ID: 39d66969ee1a25ec
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1846)) (False)
(assert (not (not (= x 1846))))

(check-sat)
(get-model)
