(set-logic ALL)
; Frontier Constraint ID: 5696c2d752b8fd8f
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2515)) (False)
(assert (not (not (= x 2515))))

(check-sat)
(get-model)
