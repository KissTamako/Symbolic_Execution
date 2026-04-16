(set-logic ALL)
; Constraint ID: 00e3464592f9a3ce
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60016)) (False)
(assert (not (not (= x 60016))))

(check-sat)
(get-model)
