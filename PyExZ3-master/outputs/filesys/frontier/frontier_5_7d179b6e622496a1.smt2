(set-logic ALL)
; Constraint ID: 7d179b6e622496a1
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59542)) (False)
(assert (not (= x 59542)))

; Query: ((== x 59543)) (False)
(assert (not (not (= x 59543))))

(check-sat)
(get-model)
