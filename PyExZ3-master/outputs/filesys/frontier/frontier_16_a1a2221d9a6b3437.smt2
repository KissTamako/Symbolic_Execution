(set-logic ALL)
; Constraint ID: a1a2221d9a6b3437
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59260)) (False)
(assert (not (not (= x 59260))))

(check-sat)
(get-model)
