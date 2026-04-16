(set-logic ALL)
; Path ID: 2ba4bc30d6f9b1e6
; Generated at: 2026-04-16 04:51:34
; Solver: Z3Wrapper
; Number of assertions: 4
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((< x 0)) (True)
(assert (< x 0))
; ((> y 0)) (False)
(assert (not (> y 0)))
; ((< x 0)) (True)
(assert (< x 0))
; ((> x 0)) (False)
(assert (not (> x 0)))

; Query: ((< y 0)) (True)
(assert (not (< y 0)))

(check-sat)
(get-model)
