(set-logic ALL)
; Constraint ID: adef3d446cc92134
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59407)) (False)
(assert (not (not (= x 59407))))

(check-sat)
(get-model)
