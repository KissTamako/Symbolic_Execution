(set-logic ALL)
; Frontier Constraint ID: 927ef4f70275faf0
; Generated at: 2026-04-17 03:12:50
; Solver: Z3Wrapper
; Number of predicates: 7
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
; ((& y 1)) (False)
(assert (not (& y 1)))

; Query: ((== (>> x 1) (>> y 1))) (False)
(assert (not (not (= (>> x 1) (>> y 1)))))

(check-sat)
(get-model)
