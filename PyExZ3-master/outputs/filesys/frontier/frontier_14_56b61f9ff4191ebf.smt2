(set-logic ALL)
; Constraint ID: 56b61f9ff4191ebf
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60532)) (False)
(assert (not (not (= x 60532))))

(check-sat)
(get-model)
