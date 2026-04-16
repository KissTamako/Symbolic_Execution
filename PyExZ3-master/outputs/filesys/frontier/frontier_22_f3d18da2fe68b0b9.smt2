(set-logic ALL)
; Frontier Constraint ID: f3d18da2fe68b0b9
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 370)) (False)
(assert (not (not (= x 370))))

(check-sat)
(get-model)
