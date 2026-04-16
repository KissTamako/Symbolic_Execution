(set-logic ALL)
; Frontier Constraint ID: 4e86ea28c7907215
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 517)) (False)
(assert (not (not (= x 517))))

(check-sat)
(get-model)
