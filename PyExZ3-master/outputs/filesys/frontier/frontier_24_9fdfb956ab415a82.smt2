(set-logic ALL)
; Constraint ID: 9fdfb956ab415a82
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59272)) (False)
(assert (not (not (= x 59272))))

(check-sat)
(get-model)
