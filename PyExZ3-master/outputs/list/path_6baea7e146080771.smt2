(set-logic ALL)
; Path ID: 6baea7e146080771
; Generated at: 2026-04-16 12:01:28
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const a Int)
(declare-const b Int)
(declare-const se Int)

; ((== a 1)) (True)
(assert (= a 1))

; Query: ((== b 2)) (True)
(assert (not (= b 2)))

(check-sat)
(get-model)
