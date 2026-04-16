(set-logic ALL)
; Frontier Constraint ID: 12451e7431b7405c
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2836)) (False)
(assert (not (not (= x 2836))))

(check-sat)
(get-model)
