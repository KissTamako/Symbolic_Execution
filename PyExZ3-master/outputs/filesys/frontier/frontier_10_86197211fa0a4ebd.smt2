(set-logic ALL)
; Frontier Constraint ID: 86197211fa0a4ebd
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2527)) (False)
(assert (not (not (= x 2527))))

(check-sat)
(get-model)
