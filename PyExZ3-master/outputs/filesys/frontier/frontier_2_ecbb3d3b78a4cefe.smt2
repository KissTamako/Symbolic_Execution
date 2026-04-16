(set-logic ALL)
; Frontier Constraint ID: ecbb3d3b78a4cefe
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 715)) (False)
(assert (not (not (= x 715))))

(check-sat)
(get-model)
