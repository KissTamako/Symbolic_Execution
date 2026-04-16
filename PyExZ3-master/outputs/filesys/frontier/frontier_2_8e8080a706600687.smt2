(set-logic ALL)
; Frontier Constraint ID: 8e8080a706600687
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1840)) (False)
(assert (not (not (= x 1840))))

(check-sat)
(get-model)
