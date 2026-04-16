(set-logic ALL)
; Frontier Constraint ID: 5b249fc7f18b5dd9
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2548)) (False)
(assert (not (not (= x 2548))))

(check-sat)
(get-model)
