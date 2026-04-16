(set-logic ALL)
; Path ID: 53797b6c16170da2
; Generated at: 2026-04-16 12:01:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const a0 Int)
(declare-const a1 Int)
(declare-const b0 Int)
(declare-const b1 Int)
(declare-const se Int)

; ((< a0 b0)) (False)
(assert (not (< a0 b0)))

; Query: ((< a1 b1)) (True)
(assert (not (< a1 b1)))

(check-sat)
(get-model)
