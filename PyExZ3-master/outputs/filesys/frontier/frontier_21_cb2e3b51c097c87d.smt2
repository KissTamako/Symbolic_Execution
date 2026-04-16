(set-logic ALL)
; Constraint ID: cb2e3b51c097c87d
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59866)) (False)
(assert (not (= x 59866)))

; Query: ((== x 59867)) (False)
(assert (not (not (= x 59867))))

(check-sat)
(get-model)
