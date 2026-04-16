(set-logic ALL)
; Frontier Constraint ID: 34648c99cfc06132
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1018)) (False)
(assert (not (= x 1018)))

; Query: ((== x 1019)) (False)
(assert (not (not (= x 1019))))

(check-sat)
(get-model)
