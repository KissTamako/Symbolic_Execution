(set-logic ALL)
; Constraint ID: db397f138225cf0c
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60616)) (False)
(assert (not (not (= x 60616))))

(check-sat)
(get-model)
