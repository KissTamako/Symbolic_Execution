(set-logic ALL)
; Frontier Constraint ID: c8d071f5c57a8b65
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 871)) (False)
(assert (not (not (= x 871))))

(check-sat)
(get-model)
