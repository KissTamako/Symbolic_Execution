(set-logic ALL)
; Constraint ID: f34565a813827448
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60301)) (False)
(assert (not (not (= x 60301))))

(check-sat)
(get-model)
