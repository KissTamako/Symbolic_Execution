(set-logic ALL)
; Executed Path ID: a602c941e80b3d41
; Generated at: 2026-04-16 16:03:05
; Solver: Z3Wrapper
; Number of predicates: 5
; Has query: False

(declare-const in1 Int)

; ((< in1 -10)) (False)
(assert (not (< in1 -10)))
; ((< in1 -5)) (False)
(assert (not (< in1 -5)))
; ((< in1 -3)) (False)
(assert (not (< in1 -3)))
; ((< in1 0)) (False)
(assert (not (< in1 0)))
; ((> in1 0)) (True)
(assert (> in1 0))

(check-sat)
(get-model)
