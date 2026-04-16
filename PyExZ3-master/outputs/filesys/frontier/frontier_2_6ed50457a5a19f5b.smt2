(set-logic ALL)
; Constraint ID: 6ed50457a5a19f5b
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59389)) (False)
(assert (not (not (= x 59389))))

(check-sat)
(get-model)
