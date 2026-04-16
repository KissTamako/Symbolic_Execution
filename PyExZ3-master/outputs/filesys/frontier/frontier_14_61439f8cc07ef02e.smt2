(set-logic ALL)
; Constraint ID: 61439f8cc07ef02e
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59257)) (False)
(assert (not (not (= x 59257))))

(check-sat)
(get-model)
