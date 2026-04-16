(set-logic ALL)
; Constraint ID: 71b8f34f62a5ac2f
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60220)) (False)
(assert (not (not (= x 60220))))

(check-sat)
(get-model)
