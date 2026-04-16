(set-logic ALL)
; Constraint ID: 89870444944f5a98
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60379)) (False)
(assert (not (not (= x 60379))))

(check-sat)
(get-model)
