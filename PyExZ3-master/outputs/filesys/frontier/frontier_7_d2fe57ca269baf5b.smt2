(set-logic ALL)
; Constraint ID: d2fe57ca269baf5b
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60520)) (False)
(assert (not (= x 60520)))

; Query: ((== x 60521)) (False)
(assert (not (not (= x 60521))))

(check-sat)
(get-model)
