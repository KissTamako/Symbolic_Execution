(set-logic ALL)
; Frontier Constraint ID: 0308586e840511fc
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
; ((& x 1)) (True)
(assert (& x 1))
; ((& y 1)) (True)
(assert (& y 1))
; ((> x y)) (False)
(assert (not (> x y)))

; Query: ((== (>> (- y x) 1) x)) (False)
(assert (not (not (= (>> (- y x) 1) x))))

(check-sat)
(get-model)
