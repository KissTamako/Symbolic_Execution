(set-logic ALL)
; Frontier Constraint ID: 8b8502a29cf0fed7
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 652)) (False)
(assert (not (not (= x 652))))

(check-sat)
(get-model)
