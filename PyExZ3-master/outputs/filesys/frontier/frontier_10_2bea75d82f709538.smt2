(set-logic ALL)
; Constraint ID: 2bea75d82f709538
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60076)) (False)
(assert (not (not (= x 60076))))

(check-sat)
(get-model)
