(set-logic ALL)
; Frontier Constraint ID: 76caee2b601bb88c
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1498)) (False)
(assert (not (not (= x 1498))))

(check-sat)
(get-model)
