(set-logic ALL)
; Frontier Constraint ID: 8c70c0e95fb417d4
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1480)) (False)
(assert (not (not (= x 1480))))

(check-sat)
(get-model)
