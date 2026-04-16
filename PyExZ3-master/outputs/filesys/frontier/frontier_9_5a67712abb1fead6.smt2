(set-logic ALL)
; Frontier Constraint ID: 5a67712abb1fead6
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 874)) (False)
(assert (not (= x 874)))

; Query: ((== x 875)) (False)
(assert (not (not (= x 875))))

(check-sat)
(get-model)
