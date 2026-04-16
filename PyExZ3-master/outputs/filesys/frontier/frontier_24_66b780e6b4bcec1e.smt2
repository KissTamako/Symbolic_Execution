(set-logic ALL)
; Constraint ID: 66b780e6b4bcec1e
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59422)) (False)
(assert (not (not (= x 59422))))

(check-sat)
(get-model)
