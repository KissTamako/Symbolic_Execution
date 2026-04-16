(set-logic ALL)
; Constraint ID: 5377f20323a73413
; Generated at: 2026-04-16 12:01:27
; Solver: Z3Wrapper
; Number of assertions: 10
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((== (- y x) 0)) (True)
(assert (= (- y x) 0))
; ((> x y)) (False)
(assert (not (> x y)))
; ((== (& y 1) 0)) (False)
(assert (not (= & 0)))
; ((== (& x 1) 0)) (False)
(assert (not (= & 0)))
; ((== (& (| x y) 1) 0)) (False)
(assert (not (= & 0)))
; ((== y 0)) (False)
(assert (not (= y 0)))
; ((== x 0)) (False)
(assert (not (= x 0)))
; ((== x y)) (True)
(assert (= x y))
; ((>= y 0)) (True)
(assert (>= y 0))
; ((>= x 0)) (True)
(assert (>= x 0))

; Query: ((!= x (<< x 0))) (False)
(assert (not (not (not (= x <<)))))

(check-sat)
(get-model)
