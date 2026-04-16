(set-logic ALL)
; Constraint ID: 00dcd8c5ee624503
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60526)) (False)
(assert (not (= x 60526)))

; Query: ((== x 60527)) (False)
(assert (not (not (= x 60527))))

(check-sat)
(get-model)
