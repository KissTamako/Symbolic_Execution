(set-logic ALL)
; Executed Path ID: 73e9ff3b90373530
; Generated at: 2026-04-17 03:12:57
; Solver: Z3Wrapper
; Number of predicates: 5
; Has query: False

(declare-const in1 Int)

; ((> in1 0)) (False)
(assert (not (> in1 0)))
; ((< in1 -10)) (False)
(assert (not (< in1 -10)))
; ((< in1 -5)) (False)
(assert (not (< in1 -5)))
; ((< in1 -3)) (False)
(assert (not (< in1 -3)))
; ((< in1 0)) (True)
(assert (< in1 0))

(check-sat)
(get-model)
