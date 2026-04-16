(set-logic ALL)
; Constraint ID: 6ce89b94f96b56cc
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59836)) (False)
(assert (not (not (= x 59836))))

(check-sat)
(get-model)
