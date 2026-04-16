(set-logic ALL)
; Executed Path ID: f20ea9a6450c322c
; Generated at: 2026-04-17 03:12:48
; Solver: Z3Wrapper
; Number of predicates: 4
; Has query: False

(declare-const x Int)

; ((>= x 0)) (False)
(assert (not (>= x 0)))
; ((> x 2)) (False)
(assert (not (> x 2)))
; ((> x 0)) (False)
(assert (not (> x 0)))
; ((> x -2)) (True)
(assert (> x -2))

(check-sat)
(get-model)
