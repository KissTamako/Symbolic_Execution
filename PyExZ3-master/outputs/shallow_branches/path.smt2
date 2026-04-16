(set-logic ALL)
; Path ID: c533a04a6601e4a1
; Generated at: 2026-04-16 12:01:32
; Solver: Z3Wrapper
; Number of assertions: 4
; Has query: True

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const in3 Int)
(declare-const in4 Int)
(declare-const in5 Int)
(declare-const se Int)

; ((== in4 0)) (False)
(assert (not (= in4 0)))
; ((== in3 0)) (False)
(assert (not (= in3 0)))
; ((== in2 0)) (False)
(assert (not (= in2 0)))
; ((== in1 0)) (False)
(assert (not (= in1 0)))

; Query: ((== in5 0)) (False)
(assert (not (not (= in5 0))))

(check-sat)
(get-model)
