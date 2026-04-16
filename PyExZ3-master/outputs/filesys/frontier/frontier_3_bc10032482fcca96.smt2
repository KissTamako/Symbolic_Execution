(set-logic ALL)
; Frontier Constraint ID: bc10032482fcca96
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 640)) (False)
(assert (not (= x 640)))

; Query: ((== x 641)) (False)
(assert (not (not (= x 641))))

(check-sat)
(get-model)
