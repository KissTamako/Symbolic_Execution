(set-logic ALL)
; Path ID: 049e8541c93d4135
; Generated at: 2026-04-16 12:01:31
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((> (* x x) 0)) (True)
(assert (not (> (* x x) 0)))

(check-sat)
(get-model)
