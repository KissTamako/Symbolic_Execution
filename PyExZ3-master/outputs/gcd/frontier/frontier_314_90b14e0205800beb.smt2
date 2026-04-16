(set-logic ALL)
; Frontier Constraint ID: 90b14e0205800beb
; Generated at: 2026-04-17 03:12:50
; Solver: Z3Wrapper
; Number of predicates: 14
; Has query: True

(declare-const x Int)
(declare-const y Int)

; ((>= x 0)) (True)
(assert (>= x 0))
; ((>= y 0)) (True)
(assert (>= y 0))
; ((== x y)) (False)
(assert (not (= x y)))
; ((== x 0)) (False)
(assert (not (= x 0)))
; ((== y 0)) (False)
(assert (not (= y 0)))
; ((& x 1)) (True)
(assert (& x 1))
; ((& y 1)) (False)
(assert (not (& y 1)))
; ((== x (>> y 1))) (True)
(assert (= x (>> y 1)))
; ((== x 0)) (False)
(assert (not (= x 0)))
; ((== y 0)) (False)
(assert (not (= y 0)))
; ((== (& (| x y) 1) 0)) (False)
(assert (not (= (& (| x y) 1) 0)))
; ((== (& x 1) 0)) (False)
(assert (not (= (& x 1) 0)))
; ((== (& y 1) 0)) (True)
(assert (= (& y 1) 0))
; ((== (& (>> y 1) 1) 0)) (False)
(assert (not (= (& (>> y 1) 1) 0)))

; Query: ((> x (>> y 1))) (False)
(assert (not (not (> x (>> y 1)))))

(check-sat)
(get-model)
