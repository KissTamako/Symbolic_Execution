(set-logic ALL)
; Constraint ID: f000950dbbaf7be4
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60232)) (False)
(assert (not (not (= x 60232))))

(check-sat)
(get-model)
