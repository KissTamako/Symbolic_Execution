(set-logic ALL)
; Frontier Constraint ID: b8d5ac9c4984ef7a
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1642)) (False)
(assert (not (not (= x 1642))))

(check-sat)
(get-model)
