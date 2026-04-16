(set-logic ALL)
; Frontier Constraint ID: a749dbe16807280f
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2455)) (False)
(assert (not (not (= x 2455))))

(check-sat)
(get-model)
