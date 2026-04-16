(set-logic ALL)
; Path ID: 6f2bea68f4151ead
; Generated at: 2026-04-16 12:01:32
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((> (+ x 1) 10)) (True)
(assert (not (> (+ x 1) 10)))

(check-sat)
(get-model)
