(set-logic ALL)
; Executed Path ID: c2c075f8a8d99b28
; Generated at: 2026-04-16 16:03:03
; Solver: Z3Wrapper
; Number of predicates: 5
; Has query: False

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const in3 Int)
(declare-const in4 Int)
(declare-const in5 Int)

; ((== in1 0)) (False)
(assert (not (= in1 0)))
; ((== in2 0)) (False)
(assert (not (= in2 0)))
; ((== in3 0)) (False)
(assert (not (= in3 0)))
; ((== in4 0)) (False)
(assert (not (= in4 0)))
; ((== in5 0)) (False)
(assert (not (= in5 0)))

(check-sat)
(get-model)
