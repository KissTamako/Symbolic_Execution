(set-logic ALL)
; Constraint ID: 9a6bb5143e0f586c
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60520)) (False)
(assert (not (not (= x 60520))))

(check-sat)
(get-model)
