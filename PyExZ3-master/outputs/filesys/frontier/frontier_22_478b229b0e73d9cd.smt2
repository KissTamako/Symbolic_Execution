(set-logic ALL)
; Frontier Constraint ID: 478b229b0e73d9cd
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2845)) (False)
(assert (not (not (= x 2845))))

(check-sat)
(get-model)
