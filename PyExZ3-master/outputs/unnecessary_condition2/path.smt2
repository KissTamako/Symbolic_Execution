(set-logic ALL)
; Path ID: b8712a8c8ad43dcb
; Generated at: 2026-04-16 12:01:33
; Solver: Z3Wrapper
; Number of assertions: 2
; Has query: True

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const se Int)

; ((< in1 5)) (False)
(assert (not (< in1 5)))
; ((> in1 in2)) (True)
(assert (> in1 in2))

; Query: ((< in1 5)) (False)
(assert (not (not (< in1 5))))

(check-sat)
(get-model)
