(set-logic ALL)
; Path ID: 8e655745a3cb89be
; Generated at: 2026-04-16 12:01:21
; Solver: Z3Wrapper
; Number of assertions: 5
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
; ((> x 0)) (False)
(assert (not (> x 0)))

; Query: ((< y 0)) (True)
(assert (not (< y 0)))

(check-sat)
(get-model)
