(set-logic ALL)
; Frontier Constraint ID: e61d0d61d82f669a
; Generated at: 2026-04-16 16:02:56
; Solver: Z3Wrapper
; Number of predicates: 12
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
; ((& y 1)) (True)
(assert (& y 1))
; ((== (>> x 1) y)) (True)
(assert (= (>> x 1) y))
; ((== x 0)) (False)
(assert (not (= x 0)))
; ((== y 0)) (False)
(assert (not (= y 0)))
; ((== (& (| x y) 1) 0)) (False)
(assert (not (= (& (| x y) 1) 0)))
; ((== (& x 1) 0)) (True)
(assert (= (& x 1) 0))

; Query: ((== (& (>> x 1) 1) 0)) (False)
(assert (not (not (= (& (>> x 1) 1) 0))))

(check-sat)
(get-model)
