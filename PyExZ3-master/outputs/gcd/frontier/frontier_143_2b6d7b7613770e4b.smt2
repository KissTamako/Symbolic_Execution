(set-logic ALL)
; Frontier Constraint ID: 2b6d7b7613770e4b
; Generated at: 2026-04-16 16:02:56
; Solver: Z3Wrapper
; Number of predicates: 10
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

; Query: ((& (>> x 1) 1)) (True)
(assert (not (& (>> x 1) 1)))

(check-sat)
(get-model)
