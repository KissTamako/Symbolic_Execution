(set-logic ALL)
; Constraint ID: 13f1d98d40a6c5b3
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60538)) (False)
(assert (not (not (= x 60538))))

(check-sat)
(get-model)
