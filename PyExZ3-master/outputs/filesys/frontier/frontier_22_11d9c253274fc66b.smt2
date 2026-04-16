(set-logic ALL)
; Constraint ID: 11d9c253274fc66b
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59569)) (False)
(assert (not (not (= x 59569))))

(check-sat)
(get-model)
