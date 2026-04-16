(set-logic ALL)
; Frontier Constraint ID: b55107b09f52e19d
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 439)) (False)
(assert (not (not (= x 439))))

(check-sat)
(get-model)
