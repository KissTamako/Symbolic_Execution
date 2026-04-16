(set-logic ALL)
; Constraint ID: 7cd0bb2f78e4eeaa
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59392)) (False)
(assert (not (not (= x 59392))))

(check-sat)
(get-model)
