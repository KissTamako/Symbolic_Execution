(set-logic ALL)
; Frontier Constraint ID: 222788ce6754a6df
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 745)) (False)
(assert (not (not (= x 745))))

(check-sat)
(get-model)
