(set-logic ALL)
; Constraint ID: c33802b5f91e8129
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60241)) (False)
(assert (not (= x 60241)))

; Query: ((== x 60242)) (False)
(assert (not (not (= x 60242))))

(check-sat)
(get-model)
