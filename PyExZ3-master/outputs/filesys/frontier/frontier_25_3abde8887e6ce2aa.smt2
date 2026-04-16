(set-logic ALL)
; Constraint ID: 3abde8887e6ce2aa
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60172)) (False)
(assert (not (= x 60172)))

; Query: ((== x 60173)) (False)
(assert (not (not (= x 60173))))

(check-sat)
(get-model)
