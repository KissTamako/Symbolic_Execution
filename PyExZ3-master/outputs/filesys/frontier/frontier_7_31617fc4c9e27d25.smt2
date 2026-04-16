(set-logic ALL)
; Constraint ID: 31617fc4c9e27d25
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59320)) (False)
(assert (not (= x 59320)))

; Query: ((== x 59321)) (False)
(assert (not (not (= x 59321))))

(check-sat)
(get-model)
