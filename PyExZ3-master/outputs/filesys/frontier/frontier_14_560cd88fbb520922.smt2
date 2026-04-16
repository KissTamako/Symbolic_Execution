(set-logic ALL)
; Constraint ID: 560cd88fbb520922
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59857)) (False)
(assert (not (not (= x 59857))))

(check-sat)
(get-model)
