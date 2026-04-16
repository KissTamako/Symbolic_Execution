(set-logic ALL)
; Path ID: 57e9f5d2b1cd1932
; Generated at: 2026-04-16 12:01:31
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== (- x 5) 0)) (True)
(assert (not (= (- x 5) 0)))

(check-sat)
(get-model)
