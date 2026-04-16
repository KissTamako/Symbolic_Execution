(set-logic ALL)
; Frontier Constraint ID: 2e4037aedaca0e2b
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 586)) (False)
(assert (not (not (= x 586))))

(check-sat)
(get-model)
