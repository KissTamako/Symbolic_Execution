(set-logic ALL)
; Constraint ID: 687f8ddc6c241d04
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60664)) (False)
(assert (not (not (= x 60664))))

(check-sat)
(get-model)
