(set-logic ALL)
; Constraint ID: 0f93cce5004f7a34
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59548)) (False)
(assert (not (= x 59548)))

; Query: ((== x 59549)) (False)
(assert (not (not (= x 59549))))

(check-sat)
(get-model)
