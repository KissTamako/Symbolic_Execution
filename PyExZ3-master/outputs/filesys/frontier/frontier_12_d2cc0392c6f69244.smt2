(set-logic ALL)
; Frontier Constraint ID: d2cc0392c6f69244
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 655)) (False)
(assert (not (not (= x 655))))

(check-sat)
(get-model)
