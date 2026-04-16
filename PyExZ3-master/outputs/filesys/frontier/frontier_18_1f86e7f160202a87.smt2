(set-logic ALL)
; Frontier Constraint ID: 1f86e7f160202a87
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 664)) (False)
(assert (not (not (= x 664))))

(check-sat)
(get-model)
