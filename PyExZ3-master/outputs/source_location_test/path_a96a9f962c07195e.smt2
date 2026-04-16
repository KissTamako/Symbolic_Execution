(set-logic ALL)
; Executed Path ID: a96a9f962c07195e
; Generated at: 2026-04-16 13:27:43
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((> x 0)) (False)
(assert (not (> x 0)))
; ((< x 0)) (False)
(assert (not (< x 0)))

(check-sat)
(get-model)
