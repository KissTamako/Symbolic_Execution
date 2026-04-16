(set-logic ALL)
; Executed Path ID: 1f838bd20cdc3fb1
; Generated at: 2026-04-17 03:12:56
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const a0 Int)
(declare-const a1 Int)
(declare-const b0 Int)
(declare-const b1 Int)

; ((< a0 b0)) (False)
(assert (not (< a0 b0)))
; ((< a1 b1)) (True)
(assert (< a1 b1))

(check-sat)
(get-model)
