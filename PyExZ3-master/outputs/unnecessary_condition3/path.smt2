(set-logic ALL)
; Path ID: bd47f5a378ee480e
; Generated at: 2026-04-16 12:01:34
; Solver: Z3Wrapper
; Number of assertions: 4
; Has query: True

(declare-const in1 Int)
(declare-const se Int)

; ((< in1 -3)) (False)
(assert (not (< in1 -3)))
; ((< in1 -5)) (False)
(assert (not (< in1 -5)))
; ((< in1 -10)) (False)
(assert (not (< in1 -10)))
; ((> in1 0)) (False)
(assert (not (> in1 0)))

; Query: ((< in1 0)) (True)
(assert (not (< in1 0)))

(check-sat)
(get-model)
