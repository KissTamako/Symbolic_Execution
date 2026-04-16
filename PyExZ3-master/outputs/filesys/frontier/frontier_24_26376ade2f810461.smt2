(set-logic ALL)
; Constraint ID: 26376ade2f810461
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60622)) (False)
(assert (not (not (= x 60622))))

(check-sat)
(get-model)
