(set-logic ALL)
; Frontier Constraint ID: f09c28f1b0e4f847
; Generated at: 2026-04-17 03:12:50
; Solver: Z3Wrapper
; Number of predicates: 16
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
; ((& x 1)) (False)
(assert (not (& x 1)))
; ((& y 1)) (False)
(assert (not (& y 1)))
; ((== (>> x 1) (>> y 1))) (False)
(assert (not (= (>> x 1) (>> y 1))))
; ((== (>> x 1) 0)) (False)
(assert (not (= (>> x 1) 0)))
; ((== (>> y 1) 0)) (False)
(assert (not (= (>> y 1) 0)))
; ((& (>> x 1) 1)) (True)
(assert (& (>> x 1) 1))
; ((& (>> y 1) 1)) (False)
(assert (not (& (>> y 1) 1)))
; ((== (>> x 1) (>> (>> y 1) 1))) (False)
(assert (not (= (>> x 1) (>> (>> y 1) 1))))
; ((== (>> x 1) 0)) (False)
(assert (not (= (>> x 1) 0)))
; ((== (>> (>> y 1) 1) 0)) (False)
(assert (not (= (>> (>> y 1) 1) 0)))
; ((& (>> x 1) 1)) (True)
(assert (& (>> x 1) 1))

; Query: ((& (>> (>> y 1) 1) 1)) (True)
(assert (not (& (>> (>> y 1) 1) 1)))

(check-sat)
(get-model)
