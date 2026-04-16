(set-logic ALL)
; Constraint ID: 3ffa1c37b39dae3e
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60466)) (False)
(assert (not (= x 60466)))

; Query: ((== x 60467)) (False)
(assert (not (not (= x 60467))))

(check-sat)
(get-model)
