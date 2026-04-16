(set-logic ALL)
; Constraint ID: f48add821cf7d956
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59701)) (False)
(assert (not (not (= x 59701))))

(check-sat)
(get-model)
