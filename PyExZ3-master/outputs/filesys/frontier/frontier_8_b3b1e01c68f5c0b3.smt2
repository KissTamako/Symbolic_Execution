(set-logic ALL)
; Frontier Constraint ID: b3b1e01c68f5c0b3
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2824)) (False)
(assert (not (not (= x 2824))))

(check-sat)
(get-model)
