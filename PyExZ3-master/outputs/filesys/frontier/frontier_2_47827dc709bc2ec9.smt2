(set-logic ALL)
; Frontier Constraint ID: 47827dc709bc2ec9
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1690)) (False)
(assert (not (not (= x 1690))))

(check-sat)
(get-model)
