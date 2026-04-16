(set-logic ALL)
; Constraint ID: ddf0c052e7929451
; Generated at: 2026-04-16 04:51:45
; Solver: Z3Wrapper
; Number of assertions: 7
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

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

; Query: ((== (>> x 1) (>> y 1))) (False)
(assert (not (not (= >> >>))))

(check-sat)
(get-model)
