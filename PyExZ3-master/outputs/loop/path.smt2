(set-logic ALL)
; Path ID: 147223f34926e0a9
; Generated at: 2026-04-16 12:01:29
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const se Int)

; ((> in1 in2)) (True)
(assert (> in1 in2))

; Query: ((> in1 0)) (False)
(assert (not (not (> in1 0))))

(check-sat)
(get-model)
