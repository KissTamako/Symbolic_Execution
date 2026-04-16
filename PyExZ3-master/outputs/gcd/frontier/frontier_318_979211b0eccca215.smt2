(set-logic ALL)
; Constraint ID: 979211b0eccca215
; Generated at: 2026-04-16 12:01:27
; Solver: Z3Wrapper
; Number of assertions: 8
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((> x y)) (False)
(assert (not (> x y)))
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

; Query: ((== (>> (- y x) 1) x)) (False)
(assert (not (not (= >> x))))

(check-sat)
(get-model)
