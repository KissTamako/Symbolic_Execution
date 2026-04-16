(set-logic ALL)
; Constraint ID: f42dca0810a61b67
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59872)) (False)
(assert (not (= x 59872)))

; Query: ((== x 59873)) (False)
(assert (not (not (= x 59873))))

(check-sat)
(get-model)
