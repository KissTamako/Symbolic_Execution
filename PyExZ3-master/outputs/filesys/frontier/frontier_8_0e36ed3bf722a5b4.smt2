(set-logic ALL)
; Constraint ID: 0e36ed3bf722a5b4
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60673)) (False)
(assert (not (not (= x 60673))))

(check-sat)
(get-model)
