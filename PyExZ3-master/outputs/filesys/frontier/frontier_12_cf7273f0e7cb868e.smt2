(set-logic ALL)
; Constraint ID: cf7273f0e7cb868e
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60454)) (False)
(assert (not (not (= x 60454))))

(check-sat)
(get-model)
