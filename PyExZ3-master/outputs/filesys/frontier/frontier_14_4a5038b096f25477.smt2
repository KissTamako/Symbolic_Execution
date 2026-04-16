(set-logic ALL)
; Constraint ID: 4a5038b096f25477
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60082)) (False)
(assert (not (not (= x 60082))))

(check-sat)
(get-model)
