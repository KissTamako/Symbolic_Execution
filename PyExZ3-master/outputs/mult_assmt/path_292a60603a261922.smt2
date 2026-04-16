(set-logic ALL)
; Path ID: 292a60603a261922
; Generated at: 2026-04-16 12:01:30
; Solver: Z3Wrapper
; Number of assertions: 2
; Has query: True

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const in3 Int)
(declare-const se Int)

; ((> in3 0)) (True)
(assert (> in3 0))
; ((== in1 in2)) (True)
(assert (= in1 in2))

; Query: ((!= (+ in1 1) in2)) (True)
(assert (not (not (= (+ in1 1) in2))))

(check-sat)
(get-model)
