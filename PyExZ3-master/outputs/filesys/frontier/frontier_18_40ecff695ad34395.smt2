(set-logic ALL)
; Constraint ID: 40ecff695ad34395
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59863)) (False)
(assert (not (not (= x 59863))))

(check-sat)
(get-model)
