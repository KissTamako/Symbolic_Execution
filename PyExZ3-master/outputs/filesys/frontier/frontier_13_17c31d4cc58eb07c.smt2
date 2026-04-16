(set-logic ALL)
; Frontier Constraint ID: 17c31d4cc58eb07c
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2530)) (False)
(assert (not (= x 2530)))

; Query: ((== x 2531)) (False)
(assert (not (not (= x 2531))))

(check-sat)
(get-model)
