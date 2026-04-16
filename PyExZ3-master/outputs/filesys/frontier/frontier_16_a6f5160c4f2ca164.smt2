(set-logic ALL)
; Frontier Constraint ID: a6f5160c4f2ca164
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1486)) (False)
(assert (not (not (= x 1486))))

(check-sat)
(get-model)
