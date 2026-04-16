(set-logic ALL)
; Executed Path ID: 1fd7ebfd142811bb
; Generated at: 2026-04-17 03:12:57
; Solver: Z3Wrapper
; Number of predicates: 3
; Has query: False

(declare-const in1 Int)
(declare-const in2 Int)

; ((> in1 in2)) (True)
(assert (> in1 in2))
; ((< in1 5)) (False)
(assert (not (< in1 5)))
; ((< in1 5)) (False)
(assert (not (< in1 5)))

(check-sat)
(get-model)
