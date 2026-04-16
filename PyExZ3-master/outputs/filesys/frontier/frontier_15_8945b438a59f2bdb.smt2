(set-logic ALL)
; Constraint ID: 8945b438a59f2bdb
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59857)) (False)
(assert (not (= x 59857)))

; Query: ((== x 59858)) (False)
(assert (not (not (= x 59858))))

(check-sat)
(get-model)
