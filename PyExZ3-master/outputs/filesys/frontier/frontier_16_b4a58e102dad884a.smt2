(set-logic ALL)
; Constraint ID: b4a58e102dad884a
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60460)) (False)
(assert (not (not (= x 60460))))

(check-sat)
(get-model)
