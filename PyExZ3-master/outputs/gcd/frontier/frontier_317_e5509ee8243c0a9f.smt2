(set-logic ALL)
; Constraint ID: e5509ee8243c0a9f
; Generated at: 2026-04-16 12:01:27
; Solver: Z3Wrapper
; Number of assertions: 7
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

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

; Query: ((> x y)) (False)
(assert (not (not (> x y))))

(check-sat)
(get-model)
