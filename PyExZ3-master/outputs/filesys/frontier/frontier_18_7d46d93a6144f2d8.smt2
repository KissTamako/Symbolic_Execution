(set-logic ALL)
; Frontier Constraint ID: 7d46d93a6144f2d8
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 589)) (False)
(assert (not (not (= x 589))))

(check-sat)
(get-model)
