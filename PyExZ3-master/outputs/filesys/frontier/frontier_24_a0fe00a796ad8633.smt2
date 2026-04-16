(set-logic ALL)
; Frontier Constraint ID: a0fe00a796ad8633
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 598)) (False)
(assert (not (not (= x 598))))

(check-sat)
(get-model)
