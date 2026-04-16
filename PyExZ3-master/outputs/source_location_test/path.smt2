(set-logic ALL)
; Path ID: aa17248d79114472
; Generated at: 2026-04-16 12:01:32
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((> x 0)) (False)
(assert (not (> x 0)))

; Query: ((< x 0)) (True)
(assert (not (< x 0)))

(check-sat)
(get-model)
