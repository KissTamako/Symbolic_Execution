(set-logic ALL)
; Constraint ID: b2edf1b2d494e1c8
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59413)) (False)
(assert (not (= x 59413)))

; Query: ((== x 59414)) (False)
(assert (not (not (= x 59414))))

(check-sat)
(get-model)
