(set-logic ALL)
; Frontier Constraint ID: 3b25d7038460e077
; Generated at: 2026-04-17 03:12:50
; Solver: Z3Wrapper
; Number of predicates: 12
; Has query: True

(declare-const x Int)
(declare-const y Int)

; ((>= x 0)) (True)
(assert (>= x 0))
; ((>= y 0)) (True)
(assert (>= y 0))
; ((== x y)) (True)
(assert (= x y))
; ((== x 0)) (False)
(assert (not (= x 0)))
; ((== y 0)) (False)
(assert (not (= y 0)))
; ((== (& (| x y) 1) 0)) (True)
(assert (= (& (| x y) 1) 0))
; ((== (& (| (>> x 1) (>> y 1)) 1) 0)) (True)
(assert (= (& (| (>> x 1) (>> y 1)) 1) 0))
; ((== (& (| (>> (>> x 1) 1) (>> (>> y 1) 1)) 1) 0)) (False)
(assert (not (= (& (| (>> (>> x 1) 1) (>> (>> y 1) 1)) 1) 0)))
; ((== (& (>> (>> x 1) 1) 1) 0)) (False)
(assert (not (= (& (>> (>> x 1) 1) 1) 0)))
; ((== (& (>> (>> y 1) 1) 1) 0)) (False)
(assert (not (= (& (>> (>> y 1) 1) 1) 0)))
; ((> (>> (>> x 1) 1) (>> (>> y 1) 1))) (False)
(assert (not (> (>> (>> x 1) 1) (>> (>> y 1) 1))))
; ((== (- (>> (>> y 1) 1) (>> (>> x 1) 1)) 0)) (True)
(assert (= (- (>> (>> y 1) 1) (>> (>> x 1) 1)) 0))

; Query: ((!= x (<< (>> (>> x 1) 1) 2))) (False)
(assert (not (not (not (= x (<< (>> (>> x 1) 1) 2))))))

(check-sat)
(get-model)
