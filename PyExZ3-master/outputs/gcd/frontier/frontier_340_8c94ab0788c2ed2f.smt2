(set-logic ALL)
; Constraint ID: 8c94ab0788c2ed2f
; Generated at: 2026-04-16 04:51:45
; Solver: Z3Wrapper
; Number of assertions: 8
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

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

; Query: ((== x 0)) (False)
(assert (not (not (= x 0))))

(check-sat)
(get-model)
