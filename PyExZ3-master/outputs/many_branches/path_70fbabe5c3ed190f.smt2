(set-logic ALL)
; Path ID: 70fbabe5c3ed190f
; Generated at: 2026-04-16 12:01:29
; Solver: Z3Wrapper
; Number of assertions: 2
; Has query: True

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const se Int)

; ((== in1 1)) (True)
(assert (= in1 1))
; ((== in1 0)) (False)
(assert (not (= in1 0)))

; Query: ((== in2 7)) (True)
(assert (not (= in2 7)))

(check-sat)
(get-model)
