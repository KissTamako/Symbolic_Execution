(set-logic ALL)
; Frontier Constraint ID: 55db08b74415b818
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 418)) (False)
(assert (not (= x 418)))

; Query: ((== x 419)) (False)
(assert (not (not (= x 419))))

(check-sat)
(get-model)
