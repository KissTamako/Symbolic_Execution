(set-logic ALL)
; Constraint ID: 96a7385747dda219
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60169)) (False)
(assert (not (not (= x 60169))))

(check-sat)
(get-model)
