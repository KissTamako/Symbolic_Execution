(set-logic ALL)
; Executed Path ID: ba1ee98fe9ad10e0
; Generated at: 2026-04-17 03:12:44
; Solver: Z3Wrapper
; Number of predicates: 6
; Has query: False

(declare-const x Int)
(declare-const y Int)

; ((> x 0)) (False)
(assert (not (> x 0)))
; ((> x 0)) (False)
(assert (not (> x 0)))
; ((< x 0)) (True)
(assert (< x 0))
; ((> y 0)) (False)
(assert (not (> y 0)))
; ((< x 0)) (True)
(assert (< x 0))
; ((< y 0)) (True)
(assert (< y 0))

(check-sat)
(get-model)
