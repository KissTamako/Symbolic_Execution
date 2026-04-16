(set-logic ALL)
; Constraint ID: caab6a2c519fa9e0
; Generated at: 2026-04-16 04:51:45
; Solver: Z3Wrapper
; Number of assertions: 16
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((== (>> (- (>> (- y x) 1) x) 1) 0)) (False)
(assert (not (= >> 0)))
; ((== (>> (- (>> (- y x) 1) x) 1) x)) (False)
(assert (not (= >> x)))
; ((> (>> (- y x) 1) x)) (True)
(assert (> >> x))
; ((& x 1)) (True)
(assert &)
; ((& (>> (- y x) 1) 1)) (True)
(assert &)
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

; Query: ((== x 0)) (False)
(assert (not (not (= x 0))))

(check-sat)
(get-model)
