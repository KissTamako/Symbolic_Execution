(set-logic ALL)
; Executed Path ID: 524b6bda01f53612
; Generated at: 2026-04-16 16:03:03
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const x Int)

; ((> (+ x 1) 10)) (True)
(assert (> (+ x 1) 10))

(check-sat)
(get-model)
