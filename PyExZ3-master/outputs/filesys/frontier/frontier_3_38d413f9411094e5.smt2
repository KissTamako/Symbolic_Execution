(set-logic ALL)
; Constraint ID: 38d413f9411094e5
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60139)) (False)
(assert (not (= x 60139)))

; Query: ((== x 60140)) (False)
(assert (not (not (= x 60140))))

(check-sat)
(get-model)
