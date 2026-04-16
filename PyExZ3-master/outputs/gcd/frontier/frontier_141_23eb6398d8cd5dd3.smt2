(set-logic ALL)
; Constraint ID: 23eb6398d8cd5dd3
; Generated at: 2026-04-16 12:01:27
; Solver: Z3Wrapper
; Number of assertions: 8
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((== (>> x 1) (>> y 1))) (False)
(assert (not (= >> >>)))
; ((& y 1)) (False)
(assert (not &))
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

; Query: ((== (>> x 1) 0)) (False)
(assert (not (not (= >> 0))))

(check-sat)
(get-model)
