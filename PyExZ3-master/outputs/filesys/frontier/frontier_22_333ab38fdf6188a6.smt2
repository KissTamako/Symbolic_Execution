(set-logic ALL)
; Constraint ID: 333ab38fdf6188a6
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60694)) (False)
(assert (not (not (= x 60694))))

(check-sat)
(get-model)
