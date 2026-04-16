(set-logic ALL)
; Frontier Constraint ID: d097f177bca6649c
; Generated at: 2026-04-16 16:02:56
; Solver: Z3Wrapper
; Number of predicates: 8
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

; Query: ((== (>> x 1) 0)) (False)
(assert (not (not (= (>> x 1) 0))))

(check-sat)
(get-model)
