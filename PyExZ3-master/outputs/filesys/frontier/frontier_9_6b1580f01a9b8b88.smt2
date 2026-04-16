(set-logic ALL)
; Constraint ID: 6b1580f01a9b8b88
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59398)) (False)
(assert (not (= x 59398)))

; Query: ((== x 59399)) (False)
(assert (not (not (= x 59399))))

(check-sat)
(get-model)
