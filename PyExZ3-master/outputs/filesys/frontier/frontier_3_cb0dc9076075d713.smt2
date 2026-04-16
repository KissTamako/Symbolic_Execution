(set-logic ALL)
; Frontier Constraint ID: cb0dc9076075d713
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 415)) (False)
(assert (not (= x 415)))

; Query: ((== x 416)) (False)
(assert (not (not (= x 416))))

(check-sat)
(get-model)
