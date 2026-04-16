(set-logic ALL)
; Frontier Constraint ID: d348fb2473bb3c5f
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1186)) (False)
(assert (not (not (= x 1186))))

(check-sat)
(get-model)
