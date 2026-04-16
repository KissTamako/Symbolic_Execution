(set-logic ALL)
; Frontier Constraint ID: a67f1c1c2b803b21
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2518)) (False)
(assert (not (not (= x 2518))))

(check-sat)
(get-model)
