(set-logic ALL)
; Constraint ID: 26a92a13d11fd1c7
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59542)) (False)
(assert (not (not (= x 59542))))

(check-sat)
(get-model)
