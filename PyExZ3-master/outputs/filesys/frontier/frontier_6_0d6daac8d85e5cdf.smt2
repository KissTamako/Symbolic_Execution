(set-logic ALL)
; Constraint ID: 0d6daac8d85e5cdf
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60670)) (False)
(assert (not (not (= x 60670))))

(check-sat)
(get-model)
