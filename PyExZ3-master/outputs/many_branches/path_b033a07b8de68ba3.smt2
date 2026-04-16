(set-logic ALL)
; Executed Path ID: b033a07b8de68ba3
; Generated at: 2026-04-16 16:03:00
; Solver: Z3Wrapper
; Number of predicates: 3
; Has query: False

(declare-const in1 Int)
(declare-const in2 Int)

; ((== in1 0)) (False)
(assert (not (= in1 0)))
; ((== in1 1)) (True)
(assert (= in1 1))
; ((== in2 7)) (True)
(assert (= in2 7))

(check-sat)
(get-model)
