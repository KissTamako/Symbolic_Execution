(set-logic ALL)
; Frontier Constraint ID: f01005c235a1779a
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2539)) (False)
(assert (not (not (= x 2539))))

(check-sat)
(get-model)
