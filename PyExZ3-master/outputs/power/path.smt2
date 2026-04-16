(set-logic ALL)
; Executed Path ID: c0ff9d60b19d088b
; Generated at: 2026-04-17 03:12:54
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const x Int)

; ((== (^ se 2) 4)) (False)
(assert (not (= (^ se 2) 4)))

(check-sat)
(get-model)
