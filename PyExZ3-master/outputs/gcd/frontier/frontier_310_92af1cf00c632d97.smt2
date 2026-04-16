(set-logic ALL)
; Frontier Constraint ID: 92af1cf00c632d97
; Generated at: 2026-04-17 03:12:50
; Solver: Z3Wrapper
; Number of predicates: 10
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
; ((& y 1)) (False)
(assert (not (& y 1)))
; ((== x (>> y 1))) (True)
(assert (= x (>> y 1)))
; ((== x 0)) (False)
(assert (not (= x 0)))
; ((== y 0)) (False)
(assert (not (= y 0)))

; Query: ((== (& (| x y) 1) 0)) (False)
(assert (not (not (= (& (| x y) 1) 0))))

(check-sat)
(get-model)
