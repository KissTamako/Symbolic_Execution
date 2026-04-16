(set-logic ALL)
; Frontier Constraint ID: b67c3b0d3a4da86b
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 343)) (False)
(assert (not (not (= x 343))))

(check-sat)
(get-model)
