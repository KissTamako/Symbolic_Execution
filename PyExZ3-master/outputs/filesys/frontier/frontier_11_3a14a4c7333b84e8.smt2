(set-logic ALL)
; Frontier Constraint ID: 3a14a4c7333b84e8
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 652)) (False)
(assert (not (= x 652)))

; Query: ((== x 653)) (False)
(assert (not (not (= x 653))))

(check-sat)
(get-model)
