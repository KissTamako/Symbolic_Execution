(set-logic ALL)
; Constraint ID: 887895c1a5360d33
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59551)) (False)
(assert (not (not (= x 59551))))

(check-sat)
(get-model)
