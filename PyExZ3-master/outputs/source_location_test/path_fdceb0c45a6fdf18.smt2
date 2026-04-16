(set-logic ALL)
; Executed Path ID: fdceb0c45a6fdf18
; Generated at: 2026-04-17 03:12:56
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((> x 0)) (False)
(assert (not (> x 0)))
; ((< x 0)) (True)
(assert (< x 0))

(check-sat)
(get-model)
