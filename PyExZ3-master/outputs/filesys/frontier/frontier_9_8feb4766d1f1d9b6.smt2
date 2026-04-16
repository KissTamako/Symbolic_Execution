(set-logic ALL)
; Frontier Constraint ID: 8feb4766d1f1d9b6
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 649)) (False)
(assert (not (= x 649)))

; Query: ((== x 650)) (False)
(assert (not (not (= x 650))))

(check-sat)
(get-model)
