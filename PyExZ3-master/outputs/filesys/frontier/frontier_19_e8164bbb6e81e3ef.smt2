(set-logic ALL)
; Frontier Constraint ID: e8164bbb6e81e3ef
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 664)) (False)
(assert (not (= x 664)))

; Query: ((== x 665)) (False)
(assert (not (not (= x 665))))

(check-sat)
(get-model)
