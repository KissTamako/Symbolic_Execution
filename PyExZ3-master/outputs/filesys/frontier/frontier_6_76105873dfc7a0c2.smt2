(set-logic ALL)
; Frontier Constraint ID: 76105873dfc7a0c2
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 496)) (False)
(assert (not (not (= x 496))))

(check-sat)
(get-model)
