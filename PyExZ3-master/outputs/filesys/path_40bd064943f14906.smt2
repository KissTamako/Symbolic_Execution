(set-logic ALL)
; Path ID: 40bd064943f14906
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59536)) (False)
(assert (not (not (= x 59536))))

(check-sat)
(get-model)
