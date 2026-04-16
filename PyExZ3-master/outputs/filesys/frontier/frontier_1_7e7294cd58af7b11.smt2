(set-logic ALL)
; Frontier Constraint ID: 7e7294cd58af7b11
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 412)) (False)
(assert (not (= x 412)))

; Query: ((== x 413)) (False)
(assert (not (not (= x 413))))

(check-sat)
(get-model)
