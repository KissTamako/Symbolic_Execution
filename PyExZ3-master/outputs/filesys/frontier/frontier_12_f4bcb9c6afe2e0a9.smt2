(set-logic ALL)
; Frontier Constraint ID: f4bcb9c6afe2e0a9
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1180)) (False)
(assert (not (not (= x 1180))))

(check-sat)
(get-model)
