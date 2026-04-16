(set-logic ALL)
; Constraint ID: 0287950ca5277111
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59707)) (False)
(assert (not (not (= x 59707))))

(check-sat)
(get-model)
