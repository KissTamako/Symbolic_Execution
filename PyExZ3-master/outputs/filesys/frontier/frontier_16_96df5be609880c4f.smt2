(set-logic ALL)
; Constraint ID: 96df5be609880c4f
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60160)) (False)
(assert (not (not (= x 60160))))

(check-sat)
(get-model)
