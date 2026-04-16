(set-logic ALL)
; Constraint ID: cf8b4b25507a766d
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59548)) (False)
(assert (not (not (= x 59548))))

(check-sat)
(get-model)
