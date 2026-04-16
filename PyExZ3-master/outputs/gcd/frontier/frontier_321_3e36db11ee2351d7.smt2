(set-logic ALL)
; Constraint ID: 3e36db11ee2351d7
; Generated at: 2026-04-16 12:01:27
; Solver: Z3Wrapper
; Number of assertions: 11
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((== x 0)) (False)
(assert (not (= x 0)))
; ((== (>> (- y x) 1) 0)) (False)
(assert (not (= >> 0)))
; ((== (>> (- y x) 1) x)) (False)
(assert (not (= >> x)))
; ((> x y)) (False)
(assert (not (> x y)))
; ((& y 1)) (True)
(assert &)
; ((& x 1)) (True)
(assert &)
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

; Query: ((& (>> (- y x) 1) 1)) (True)
(assert (not &))

(check-sat)
(get-model)
