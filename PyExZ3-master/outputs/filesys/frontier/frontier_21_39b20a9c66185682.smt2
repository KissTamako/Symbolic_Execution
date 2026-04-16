(set-logic ALL)
; Constraint ID: 39b20a9c66185682
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59566)) (False)
(assert (not (= x 59566)))

; Query: ((== x 59567)) (False)
(assert (not (not (= x 59567))))

(check-sat)
(get-model)
