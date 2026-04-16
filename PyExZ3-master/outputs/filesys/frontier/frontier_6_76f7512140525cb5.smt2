(set-logic ALL)
; Constraint ID: 76f7512140525cb5
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60595)) (False)
(assert (not (not (= x 60595))))

(check-sat)
(get-model)
