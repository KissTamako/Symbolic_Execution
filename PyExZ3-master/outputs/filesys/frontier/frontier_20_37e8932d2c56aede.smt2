(set-logic ALL)
; Constraint ID: 37e8932d2c56aede
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60391)) (False)
(assert (not (not (= x 60391))))

(check-sat)
(get-model)
