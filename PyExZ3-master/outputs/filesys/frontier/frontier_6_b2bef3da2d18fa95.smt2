(set-logic ALL)
; Constraint ID: b2bef3da2d18fa95
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59695)) (False)
(assert (not (not (= x 59695))))

(check-sat)
(get-model)
