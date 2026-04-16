(set-logic ALL)
; Constraint ID: 6380f4bae617c331
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60523)) (False)
(assert (not (not (= x 60523))))

(check-sat)
(get-model)
