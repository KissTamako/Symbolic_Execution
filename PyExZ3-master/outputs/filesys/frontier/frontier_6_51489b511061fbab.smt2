(set-logic ALL)
; Constraint ID: 51489b511061fbab
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59245)) (False)
(assert (not (not (= x 59245))))

(check-sat)
(get-model)
