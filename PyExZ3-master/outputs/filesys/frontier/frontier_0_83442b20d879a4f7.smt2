(set-logic ALL)
; Constraint ID: 83442b20d879a4f7
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59686)) (False)
(assert (not (not (= x 59686))))

(check-sat)
(get-model)
