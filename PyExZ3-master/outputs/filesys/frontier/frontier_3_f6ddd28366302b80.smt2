(set-logic ALL)
; Constraint ID: f6ddd28366302b80
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59914)) (False)
(assert (not (= x 59914)))

; Query: ((== x 59915)) (False)
(assert (not (not (= x 59915))))

(check-sat)
(get-model)
