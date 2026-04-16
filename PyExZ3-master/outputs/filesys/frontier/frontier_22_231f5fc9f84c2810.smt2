(set-logic ALL)
; Constraint ID: 231f5fc9f84c2810
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60094)) (False)
(assert (not (not (= x 60094))))

(check-sat)
(get-model)
