(set-logic ALL)
; Frontier Constraint ID: 550f6aa5b1fc727d
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1873)) (False)
(assert (not (not (= x 1873))))

(check-sat)
(get-model)
