(set-logic ALL)
; Constraint ID: 85fbfde795568f6e
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59644)) (False)
(assert (not (not (= x 59644))))

(check-sat)
(get-model)
