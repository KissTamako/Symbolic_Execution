(set-logic ALL)
; Frontier Constraint ID: 8c05f69f723c77c2
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1702)) (False)
(assert (not (not (= x 1702))))

(check-sat)
(get-model)
