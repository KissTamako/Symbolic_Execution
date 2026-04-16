(set-logic ALL)
; Constraint ID: 16ed2604241f95fa
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59416)) (False)
(assert (not (not (= x 59416))))

(check-sat)
(get-model)
