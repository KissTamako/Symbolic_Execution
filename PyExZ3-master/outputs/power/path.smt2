(set-logic ALL)
; Path ID: 12136937339d7b21
; Generated at: 2026-04-16 12:01:31
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)


; Query: ((== (^ se 2) 4)) (False)
(assert (not (not (= ^ 4))))

(check-sat)
(get-model)
