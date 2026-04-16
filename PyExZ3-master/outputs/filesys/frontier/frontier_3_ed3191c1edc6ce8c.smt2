(set-logic ALL)
; Constraint ID: ed3191c1edc6ce8c
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59539)) (False)
(assert (not (= x 59539)))

; Query: ((== x 59540)) (False)
(assert (not (not (= x 59540))))

(check-sat)
(get-model)
