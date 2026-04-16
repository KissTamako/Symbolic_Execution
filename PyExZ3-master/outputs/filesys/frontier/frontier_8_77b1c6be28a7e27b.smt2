(set-logic ALL)
; Constraint ID: 77b1c6be28a7e27b
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60448)) (False)
(assert (not (not (= x 60448))))

(check-sat)
(get-model)
