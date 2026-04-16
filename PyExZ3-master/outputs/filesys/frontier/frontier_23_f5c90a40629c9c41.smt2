(set-logic ALL)
; Constraint ID: f5c90a40629c9c41
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59269)) (False)
(assert (not (= x 59269)))

; Query: ((== x 59270)) (False)
(assert (not (not (= x 59270))))

(check-sat)
(get-model)
