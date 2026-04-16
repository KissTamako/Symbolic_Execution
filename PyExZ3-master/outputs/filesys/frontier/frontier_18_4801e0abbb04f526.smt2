(set-logic ALL)
; Frontier Constraint ID: 4801e0abbb04f526
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 364)) (False)
(assert (not (not (= x 364))))

(check-sat)
(get-model)
