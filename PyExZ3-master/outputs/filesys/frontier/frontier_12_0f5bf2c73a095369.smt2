(set-logic ALL)
; Constraint ID: 0f5bf2c73a095369
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59704)) (False)
(assert (not (not (= x 59704))))

(check-sat)
(get-model)
