(set-logic ALL)
; Frontier Constraint ID: d1cd5458ca2db799
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2833)) (False)
(assert (not (not (= x 2833))))

(check-sat)
(get-model)
