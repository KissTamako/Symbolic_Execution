(set-logic ALL)
; Frontier Constraint ID: 6898d5ff04060cab
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1198)) (False)
(assert (not (not (= x 1198))))

(check-sat)
(get-model)
