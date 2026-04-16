(set-logic ALL)
; Constraint ID: f2ca81f8e96dba01
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59722)) (False)
(assert (not (not (= x 59722))))

(check-sat)
(get-model)
