(set-logic ALL)
; Path ID: 2083d1a0181e4bc1
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59611)) (False)
(assert (not (not (= x 59611))))

(check-sat)
(get-model)
