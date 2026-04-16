(set-logic ALL)
; Frontier Constraint ID: 15e84be0b4d462ca
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 343)) (False)
(assert (not (= x 343)))

; Query: ((== x 344)) (False)
(assert (not (not (= x 344))))

(check-sat)
(get-model)
