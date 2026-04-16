(set-logic ALL)
; Constraint ID: 88acfbc348613978
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60661)) (False)
(assert (not (= x 60661)))

; Query: ((== x 60662)) (False)
(assert (not (not (= x 60662))))

(check-sat)
(get-model)
