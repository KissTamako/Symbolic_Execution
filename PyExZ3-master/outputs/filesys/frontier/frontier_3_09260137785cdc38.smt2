(set-logic ALL)
; Frontier Constraint ID: 09260137785cdc38
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2515)) (False)
(assert (not (= x 2515)))

; Query: ((== x 2516)) (False)
(assert (not (not (= x 2516))))

(check-sat)
(get-model)
