(set-logic ALL)
; Path ID: bc05f135d5214a82
; Generated at: 2026-04-16 12:01:23
; Solver: Z3Wrapper
; Number of assertions: 8
; Has query: True

(declare-const in1 Int)
(declare-const se Int)

; ((== in1 7)) (False)
(assert (not (= in1 7)))
; ((== in1 6)) (False)
(assert (not (= in1 6)))
; ((== in1 5)) (False)
(assert (not (= in1 5)))
; ((== in1 4)) (False)
(assert (not (= in1 4)))
; ((== in1 3)) (False)
(assert (not (= in1 3)))
; ((== in1 2)) (False)
(assert (not (= in1 2)))
; ((== in1 1)) (False)
(assert (not (= in1 1)))
; ((== in1 0)) (False)
(assert (not (= in1 0)))

; Query: ((== in1 8)) (False)
(assert (not (not (= in1 8))))

(check-sat)
(get-model)
