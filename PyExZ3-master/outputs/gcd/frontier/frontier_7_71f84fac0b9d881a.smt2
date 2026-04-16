(set-logic ALL)
; Constraint ID: 71f84fac0b9d881a
; Generated at: 2026-04-16 12:01:27
; Solver: Z3Wrapper
; Number of assertions: 7
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

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

; Query: ((== (& y 1) 0)) (False)
(assert (not (not (= & 0))))

(check-sat)
(get-model)
