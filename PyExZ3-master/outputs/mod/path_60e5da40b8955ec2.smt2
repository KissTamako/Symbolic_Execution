(set-logic ALL)
; Executed Path ID: 60e5da40b8955ec2
; Generated at: 2026-04-16 16:03:01
; Solver: Z3Wrapper
; Number of predicates: 3
; Has query: False

(declare-const x Int)
(declare-const y Int)

; ((> y 0)) (True)
(assert (> y 0))
; ((< y 10)) (True)
(assert (< y 10))
; ((== (% x (+ y 1)) 3)) (True)
(assert (= (mod x (+ y 1)) 3))

(check-sat)
(get-model)
