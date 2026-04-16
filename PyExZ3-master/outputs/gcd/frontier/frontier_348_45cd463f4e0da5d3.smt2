(set-logic ALL)
; Constraint ID: 45cd463f4e0da5d3
; Generated at: 2026-04-16 04:51:45
; Solver: Z3Wrapper
; Number of assertions: 16
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((== (- (>> y 1) x) 0)) (True)
(assert (= (- >> x) 0))
; ((> x (>> y 1))) (False)
(assert (not (> x >>)))
; ((== (& (>> y 1) 1) 0)) (False)
(assert (not (= & 0)))
; ((== (& y 1) 0)) (True)
(assert (= & 0))
; ((== (& x 1) 0)) (False)
(assert (not (= & 0)))
; ((== (& (| x y) 1) 0)) (False)
(assert (not (= & 0)))
; ((== y 0)) (False)
(assert (not (= y 0)))
; ((== x 0)) (False)
(assert (not (= x 0)))
; ((== x (>> y 1))) (True)
(assert (= x >>))
; ((& y 1)) (False)
(assert (not &))
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

; Query: ((!= x (<< x 0))) (False)
(assert (not (not (not (= x <<)))))

(check-sat)
(get-model)
