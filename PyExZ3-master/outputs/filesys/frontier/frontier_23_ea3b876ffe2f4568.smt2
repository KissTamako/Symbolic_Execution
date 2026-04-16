(set-logic ALL)
; Frontier Constraint ID: ea3b876ffe2f4568
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 895)) (False)
(assert (not (= x 895)))

; Query: ((== x 896)) (False)
(assert (not (not (= x 896))))

(check-sat)
(get-model)
