(set-logic ALL)
; Constraint ID: 614b179b3059e2c4
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59944)) (False)
(assert (not (not (= x 59944))))

(check-sat)
(get-model)
