(set-logic ALL)
; Constraint ID: 96776df3167d1ddf
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59647)) (False)
(assert (not (not (= x 59647))))

(check-sat)
(get-model)
