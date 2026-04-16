(set-logic ALL)
; Frontier Constraint ID: 92d356707da6e173
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 427)) (False)
(assert (not (not (= x 427))))

(check-sat)
(get-model)
