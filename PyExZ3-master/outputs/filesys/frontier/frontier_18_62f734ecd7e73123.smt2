(set-logic ALL)
; Constraint ID: 62f734ecd7e73123
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60388)) (False)
(assert (not (not (= x 60388))))

(check-sat)
(get-model)
