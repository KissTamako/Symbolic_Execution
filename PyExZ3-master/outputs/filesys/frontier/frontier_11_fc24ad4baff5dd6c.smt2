(set-logic ALL)
; Frontier Constraint ID: fc24ad4baff5dd6c
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1702)) (False)
(assert (not (= x 1702)))

; Query: ((== x 1703)) (False)
(assert (not (not (= x 1703))))

(check-sat)
(get-model)
