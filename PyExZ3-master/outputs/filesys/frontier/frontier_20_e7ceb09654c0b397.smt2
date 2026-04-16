(set-logic ALL)
; Frontier Constraint ID: e7ceb09654c0b397
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 667)) (False)
(assert (not (not (= x 667))))

(check-sat)
(get-model)
