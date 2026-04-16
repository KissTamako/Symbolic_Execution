(set-logic ALL)
; Constraint ID: 1cfc053d303103f5
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60211)) (False)
(assert (not (not (= x 60211))))

(check-sat)
(get-model)
