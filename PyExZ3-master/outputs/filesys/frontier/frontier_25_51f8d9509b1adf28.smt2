(set-logic ALL)
; Constraint ID: 51f8d9509b1adf28
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60097)) (False)
(assert (not (= x 60097)))

; Query: ((== x 60098)) (False)
(assert (not (not (= x 60098))))

(check-sat)
(get-model)
