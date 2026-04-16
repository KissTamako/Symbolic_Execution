(set-logic ALL)
; Frontier Constraint ID: a0ae989adc20fa4b
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 571)) (False)
(assert (not (not (= x 571))))

(check-sat)
(get-model)
