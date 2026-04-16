(set-logic ALL)
; Constraint ID: cbf862fa45f15a21
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60241)) (False)
(assert (not (not (= x 60241))))

(check-sat)
(get-model)
