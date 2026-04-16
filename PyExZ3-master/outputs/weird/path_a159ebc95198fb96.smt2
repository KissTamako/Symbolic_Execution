(set-logic ALL)
; Path ID: a159ebc95198fb96
; Generated at: 2026-04-16 12:01:34
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)


; Query: ((== (+ (< x y) x) 1)) (True)
(assert (not (= (+ (< x y) x) 1)))

(check-sat)
(get-model)
