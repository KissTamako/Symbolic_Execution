(set-logic ALL)
; Frontier Constraint ID: e86042ff3a0319f8
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 637)) (False)
(assert (not (not (= x 637))))

(check-sat)
(get-model)
