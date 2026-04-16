(set-logic ALL)
; Frontier Constraint ID: f14998fe6c6dd0b4
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1639)) (False)
(assert (not (not (= x 1639))))

(check-sat)
(get-model)
