(set-logic ALL)
; Executed Path ID: eafb572dbb2a4616
; Generated at: 2026-04-16 16:02:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const a Int)

; ((< (+ a 1) a)) (False)
(assert (not (< (+ a 1) a)))

(check-sat)
(get-model)
