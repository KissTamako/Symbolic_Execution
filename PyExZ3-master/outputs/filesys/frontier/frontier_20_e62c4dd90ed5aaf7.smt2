(set-logic ALL)
; Constraint ID: e62c4dd90ed5aaf7
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59566)) (False)
(assert (not (not (= x 59566))))

(check-sat)
(get-model)
