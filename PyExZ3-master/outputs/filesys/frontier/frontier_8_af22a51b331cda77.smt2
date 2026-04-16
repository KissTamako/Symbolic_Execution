(set-logic ALL)
; Constraint ID: af22a51b331cda77
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59698)) (False)
(assert (not (not (= x 59698))))

(check-sat)
(get-model)
