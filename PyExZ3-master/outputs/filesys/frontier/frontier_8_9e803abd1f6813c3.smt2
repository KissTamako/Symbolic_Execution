(set-logic ALL)
; Constraint ID: 9e803abd1f6813c3
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59848)) (False)
(assert (not (not (= x 59848))))

(check-sat)
(get-model)
