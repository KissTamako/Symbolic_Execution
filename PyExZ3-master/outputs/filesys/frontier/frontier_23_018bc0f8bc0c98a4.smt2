(set-logic ALL)
; Constraint ID: 018bc0f8bc0c98a4
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59494)) (False)
(assert (not (= x 59494)))

; Query: ((== x 59495)) (False)
(assert (not (not (= x 59495))))

(check-sat)
(get-model)
