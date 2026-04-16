(set-logic ALL)
; Frontier Constraint ID: 3c2c867a2694599d
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2461)) (False)
(assert (not (not (= x 2461))))

(check-sat)
(get-model)
