(set-logic ALL)
; Path ID: ad576e1625f34d91
; Generated at: 2026-04-16 12:01:34
; Solver: Z3Wrapper
; Number of assertions: 4
; Has query: True

(declare-const in1 Int)
(declare-const se Int)

; ((< in1 0)) (False)
(assert (not (< in1 0)))
; ((< in1 -3)) (False)
(assert (not (< in1 -3)))
; ((< in1 -5)) (False)
(assert (not (< in1 -5)))
; ((< in1 -10)) (False)
(assert (not (< in1 -10)))

; Query: ((> in1 0)) (True)
(assert (not (> in1 0)))

(check-sat)
(get-model)
