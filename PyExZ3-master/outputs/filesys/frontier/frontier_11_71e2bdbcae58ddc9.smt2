(set-logic ALL)
; Frontier Constraint ID: 71e2bdbcae58ddc9
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 727)) (False)
(assert (not (= x 727)))

; Query: ((== x 728)) (False)
(assert (not (not (= x 728))))

(check-sat)
(get-model)
