(set-logic ALL)
; Path ID: afcde3e2425d6d48
; Generated at: 2026-04-16 12:01:33
; Solver: Z3Wrapper
; Number of assertions: 2
; Has query: True

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const se Int)

; ((< in1 in2)) (False)
(assert (not (< in1 in2)))
; ((> in1 in2)) (True)
(assert (> in1 in2))

; Query: ((< in1 in2)) (False)
(assert (not (not (< in1 in2))))

(check-sat)
(get-model)
