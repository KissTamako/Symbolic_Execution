(set-logic ALL)
; Constraint ID: eb9790787414d0fa
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59635)) (False)
(assert (not (not (= x 59635))))

(check-sat)
(get-model)
