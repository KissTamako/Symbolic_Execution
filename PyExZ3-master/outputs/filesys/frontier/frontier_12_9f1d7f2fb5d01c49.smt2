(set-logic ALL)
; Constraint ID: 9f1d7f2fb5d01c49
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59479)) (False)
(assert (not (not (= x 59479))))

(check-sat)
(get-model)
