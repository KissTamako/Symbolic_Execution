(set-logic ALL)
; Constraint ID: e0793d98be14b58e
; Generated at: 2026-04-16 04:51:45
; Solver: Z3Wrapper
; Number of assertions: 9
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((== x 0)) (False)
(assert (not (= x 0)))
; ((== (>> x 1) y)) (True)
(assert (= >> y))
; ((& y 1)) (True)
(assert &)
; ((& x 1)) (False)
(assert (not &))
; ((== y 0)) (False)
(assert (not (= y 0)))
; ((== x 0)) (False)
(assert (not (= x 0)))
; ((== x y)) (False)
(assert (not (= x y)))
; ((>= y 0)) (True)
(assert (>= y 0))
; ((>= x 0)) (True)
(assert (>= x 0))

; Query: ((== y 0)) (False)
(assert (not (not (= y 0))))

(check-sat)
(get-model)
