(set-logic ALL)
; Constraint ID: 7af4cb2c9f7cbd70
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59620)) (False)
(assert (not (not (= x 59620))))

(check-sat)
(get-model)
