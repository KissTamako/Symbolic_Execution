(set-logic ALL)
; Frontier Constraint ID: b510048de642c757
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 661)) (False)
(assert (not (= x 661)))

; Query: ((== x 662)) (False)
(assert (not (not (= x 662))))

(check-sat)
(get-model)
