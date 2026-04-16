(set-logic ALL)
; Executed Path ID: ce7220da88099898
; Generated at: 2026-04-16 16:03:01
; Solver: Z3Wrapper
; Number of predicates: 3
; Has query: False

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const in3 Int)

; ((== in1 in2)) (True)
(assert (= in1 in2))
; ((> in3 0)) (True)
(assert (> in3 0))
; ((!= (+ in1 1) in2)) (True)
(assert (not (= (+ in1 1) in2)))

(check-sat)
(get-model)
