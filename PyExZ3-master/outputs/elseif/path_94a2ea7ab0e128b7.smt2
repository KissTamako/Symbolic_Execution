(set-logic ALL)
; Executed Path ID: 94a2ea7ab0e128b7
; Generated at: 2026-04-16 16:02:52
; Solver: Z3Wrapper
; Number of predicates: 9
; Has query: False

(declare-const in1 Int)

; ((== in1 0)) (False)
(assert (not (= in1 0)))
; ((== in1 1)) (False)
(assert (not (= in1 1)))
; ((== in1 2)) (False)
(assert (not (= in1 2)))
; ((== in1 3)) (False)
(assert (not (= in1 3)))
; ((== in1 4)) (False)
(assert (not (= in1 4)))
; ((== in1 5)) (False)
(assert (not (= in1 5)))
; ((== in1 6)) (False)
(assert (not (= in1 6)))
; ((== in1 7)) (False)
(assert (not (= in1 7)))
; ((== in1 8)) (False)
(assert (not (= in1 8)))

(check-sat)
(get-model)
