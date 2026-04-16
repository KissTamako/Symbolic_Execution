(set-logic ALL)
; Constraint ID: c523b907527cda1c
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60442)) (False)
(assert (not (= x 60442)))

; Query: ((== x 60443)) (False)
(assert (not (not (= x 60443))))

(check-sat)
(get-model)
