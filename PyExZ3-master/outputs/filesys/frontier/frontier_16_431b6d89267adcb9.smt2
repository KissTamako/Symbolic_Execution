(set-logic ALL)
; Frontier Constraint ID: 431b6d89267adcb9
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 661)) (False)
(assert (not (not (= x 661))))

(check-sat)
(get-model)
