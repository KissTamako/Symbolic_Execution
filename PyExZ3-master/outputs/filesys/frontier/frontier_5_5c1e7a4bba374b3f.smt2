(set-logic ALL)
; Constraint ID: 5c1e7a4bba374b3f
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60292)) (False)
(assert (not (= x 60292)))

; Query: ((== x 60293)) (False)
(assert (not (not (= x 60293))))

(check-sat)
(get-model)
