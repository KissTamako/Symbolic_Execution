(set-logic ALL)
; Frontier Constraint ID: 936b5f51b708ea51
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1630)) (False)
(assert (not (not (= x 1630))))

(check-sat)
(get-model)
