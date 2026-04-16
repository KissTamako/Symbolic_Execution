(set-logic ALL)
; Frontier Constraint ID: af08acb96d0fd579
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 733)) (False)
(assert (not (not (= x 733))))

(check-sat)
(get-model)
