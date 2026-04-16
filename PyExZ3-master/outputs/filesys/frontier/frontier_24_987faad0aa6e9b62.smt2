(set-logic ALL)
; Constraint ID: 987faad0aa6e9b62
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59872)) (False)
(assert (not (not (= x 59872))))

(check-sat)
(get-model)
