(set-logic ALL)
; Constraint ID: d8bf585f1b1fef62
; Generated at: 2026-04-16 12:01:27
; Solver: Z3Wrapper
; Number of assertions: 16
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((& (>> x 1) 1)) (True)
(assert &)
; ((== (>> (>> y 1) 1) 0)) (False)
(assert (not (= >> 0)))
; ((== (>> x 1) 0)) (False)
(assert (not (= >> 0)))
; ((== (>> x 1) (>> (>> y 1) 1))) (False)
(assert (not (= >> >>)))
; ((& (>> y 1) 1)) (False)
(assert (not &))
; ((& (>> x 1) 1)) (True)
(assert &)
; ((== (>> y 1) 0)) (False)
(assert (not (= >> 0)))
; ((== (>> x 1) 0)) (False)
(assert (not (= >> 0)))
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

; Query: ((& (>> (>> y 1) 1) 1)) (True)
(assert (not &))

(check-sat)
(get-model)
