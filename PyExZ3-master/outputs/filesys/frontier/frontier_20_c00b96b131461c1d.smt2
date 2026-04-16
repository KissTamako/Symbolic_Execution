(set-logic ALL)
; Constraint ID: c00b96b131461c1d
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60466)) (False)
(assert (not (not (= x 60466))))

(check-sat)
(get-model)
