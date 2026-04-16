(set-logic ALL)
; Constraint ID: 103e528b0135a727
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60010)) (False)
(assert (not (not (= x 60010))))

(check-sat)
(get-model)
