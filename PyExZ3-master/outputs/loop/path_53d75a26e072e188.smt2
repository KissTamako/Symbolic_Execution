(set-logic ALL)
; Executed Path ID: 53d75a26e072e188
; Generated at: 2026-04-17 03:12:53
; Solver: Z3Wrapper
; Number of predicates: 3
; Has query: False

(declare-const in1 Int)
(declare-const in2 Int)

; ((> in1 in2)) (True)
(assert (> in1 in2))
; ((> in1 0)) (False)
(assert (not (> in1 0)))
; ((> in1 0)) (False)
(assert (not (> in1 0)))

(check-sat)
(get-model)
