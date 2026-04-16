(set-logic ALL)
; Frontier Constraint ID: 2d500a935537cf0c
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2440)) (False)
(assert (not (not (= x 2440))))

(check-sat)
(get-model)
