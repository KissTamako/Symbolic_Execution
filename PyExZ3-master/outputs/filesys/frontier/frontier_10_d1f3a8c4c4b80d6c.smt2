(set-logic ALL)
; Frontier Constraint ID: d1f3a8c4c4b80d6c
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 577)) (False)
(assert (not (not (= x 577))))

(check-sat)
(get-model)
