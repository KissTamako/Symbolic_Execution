(set-logic ALL)
; Constraint ID: 67d4b7b65b3a2d09
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59707)) (False)
(assert (not (= x 59707)))

; Query: ((== x 59708)) (False)
(assert (not (not (= x 59708))))

(check-sat)
(get-model)
