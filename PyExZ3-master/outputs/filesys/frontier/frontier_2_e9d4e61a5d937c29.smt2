(set-logic ALL)
; Constraint ID: e9d4e61a5d937c29
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59839)) (False)
(assert (not (not (= x 59839))))

(check-sat)
(get-model)
