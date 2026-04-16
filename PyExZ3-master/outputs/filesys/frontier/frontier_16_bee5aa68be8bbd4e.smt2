(set-logic ALL)
; Constraint ID: bee5aa68be8bbd4e
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60085)) (False)
(assert (not (not (= x 60085))))

(check-sat)
(get-model)
