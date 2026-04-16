(set-logic ALL)
; Constraint ID: 656a635b2cdd46a5
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59545)) (False)
(assert (not (not (= x 59545))))

(check-sat)
(get-model)
