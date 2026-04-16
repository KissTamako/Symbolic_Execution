(set-logic ALL)
; Frontier Constraint ID: e3673fe707abd962
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1189)) (False)
(assert (not (not (= x 1189))))

(check-sat)
(get-model)
