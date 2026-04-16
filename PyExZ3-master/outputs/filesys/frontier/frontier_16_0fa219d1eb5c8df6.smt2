(set-logic ALL)
; Frontier Constraint ID: 0fa219d1eb5c8df6
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1336)) (False)
(assert (not (not (= x 1336))))

(check-sat)
(get-model)
