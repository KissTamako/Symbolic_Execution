(set-logic ALL)
; Frontier Constraint ID: 83c6e36c16a8be91
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1621)) (False)
(assert (not (not (= x 1621))))

(check-sat)
(get-model)
