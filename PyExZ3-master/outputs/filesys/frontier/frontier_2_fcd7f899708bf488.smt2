(set-logic ALL)
; Frontier Constraint ID: fcd7f899708bf488
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1615)) (False)
(assert (not (not (= x 1615))))

(check-sat)
(get-model)
