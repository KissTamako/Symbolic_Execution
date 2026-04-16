(set-logic ALL)
; Frontier Constraint ID: 9a5d7cba59a7c83b
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2839)) (False)
(assert (not (not (= x 2839))))

(check-sat)
(get-model)
