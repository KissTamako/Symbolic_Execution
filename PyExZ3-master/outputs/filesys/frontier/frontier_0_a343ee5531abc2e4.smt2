(set-logic ALL)
; Frontier Constraint ID: a343ee5531abc2e4
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 487)) (False)
(assert (not (not (= x 487))))

(check-sat)
(get-model)
