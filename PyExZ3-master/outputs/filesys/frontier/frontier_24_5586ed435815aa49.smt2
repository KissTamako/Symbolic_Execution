(set-logic ALL)
; Constraint ID: 5586ed435815aa49
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60397)) (False)
(assert (not (not (= x 60397))))

(check-sat)
(get-model)
