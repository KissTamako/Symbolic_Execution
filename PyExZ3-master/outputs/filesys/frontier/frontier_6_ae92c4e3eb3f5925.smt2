(set-logic ALL)
; Constraint ID: ae92c4e3eb3f5925
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59320)) (False)
(assert (not (not (= x 59320))))

(check-sat)
(get-model)
