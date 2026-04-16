(set-logic ALL)
; Frontier Constraint ID: 8d7f703df49cdc12
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2821)) (False)
(assert (not (not (= x 2821))))

(check-sat)
(get-model)
