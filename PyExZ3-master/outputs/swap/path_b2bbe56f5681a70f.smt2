(set-logic ALL)
; Path ID: b2bbe56f5681a70f
; Generated at: 2026-04-16 12:01:32
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const se Int)

; ((> in1 in2)) (True)
(assert (> in1 in2))

; Query: ((> (^ (^ in1 in2) (^ (^ in1 in2) in2)) (^ (^ in1 in2) in2))) (False)
(assert (not (not (> ^ ^))))

(check-sat)
(get-model)
