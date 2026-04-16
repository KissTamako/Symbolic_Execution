(set-logic ALL)
; Frontier Constraint ID: 2b7d1f8489e35d7c
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1198)) (False)
(assert (not (= x 1198)))

; Query: ((== x 1199)) (False)
(assert (not (not (= x 1199))))

(check-sat)
(get-model)
