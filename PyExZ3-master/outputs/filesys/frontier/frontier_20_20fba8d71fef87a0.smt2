(set-logic ALL)
; Frontier Constraint ID: 20fba8d71fef87a0
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1342)) (False)
(assert (not (not (= x 1342))))

(check-sat)
(get-model)
