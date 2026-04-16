(set-logic ALL)
; Path ID: 351447582b0157b7
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60436)) (False)
(assert (not (not (= x 60436))))

(check-sat)
(get-model)
