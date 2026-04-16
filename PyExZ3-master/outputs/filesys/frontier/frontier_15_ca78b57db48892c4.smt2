(set-logic ALL)
; Constraint ID: ca78b57db48892c4
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59332)) (False)
(assert (not (= x 59332)))

; Query: ((== x 59333)) (False)
(assert (not (not (= x 59333))))

(check-sat)
(get-model)
