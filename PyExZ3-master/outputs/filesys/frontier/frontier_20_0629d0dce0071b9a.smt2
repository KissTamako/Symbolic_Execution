(set-logic ALL)
; Frontier Constraint ID: 0629d0dce0071b9a
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 892)) (False)
(assert (not (not (= x 892))))

(check-sat)
(get-model)
