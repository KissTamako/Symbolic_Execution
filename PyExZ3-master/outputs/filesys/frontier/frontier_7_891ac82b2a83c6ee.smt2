(set-logic ALL)
; Frontier Constraint ID: 891ac82b2a83c6ee
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1846)) (False)
(assert (not (= x 1846)))

; Query: ((== x 1847)) (False)
(assert (not (not (= x 1847))))

(check-sat)
(get-model)
