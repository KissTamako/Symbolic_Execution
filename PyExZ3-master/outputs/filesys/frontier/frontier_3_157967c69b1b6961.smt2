(set-logic ALL)
; Constraint ID: 157967c69b1b6961
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59239)) (False)
(assert (not (= x 59239)))

; Query: ((== x 59240)) (False)
(assert (not (not (= x 59240))))

(check-sat)
(get-model)
