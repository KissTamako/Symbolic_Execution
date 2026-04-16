(set-logic ALL)
; Constraint ID: ece07abcb2c83a3b
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60397)) (False)
(assert (not (= x 60397)))

; Query: ((== x 60398)) (False)
(assert (not (not (= x 60398))))

(check-sat)
(get-model)
