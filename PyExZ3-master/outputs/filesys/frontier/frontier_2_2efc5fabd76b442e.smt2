(set-logic ALL)
; Frontier Constraint ID: 2efc5fabd76b442e
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 565)) (False)
(assert (not (not (= x 565))))

(check-sat)
(get-model)
