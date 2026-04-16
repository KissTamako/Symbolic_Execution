(set-logic ALL)
; Frontier Constraint ID: 94c975bf06474b1a
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1483)) (False)
(assert (not (not (= x 1483))))

(check-sat)
(get-model)
