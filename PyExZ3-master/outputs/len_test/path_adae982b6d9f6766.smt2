(set-logic ALL)
; Path ID: adae982b6d9f6766
; Generated at: 2026-04-16 12:01:28
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const a Int)
(declare-const se Int)


; Query: ((== a 2)) (True)
(assert (not (= a 2)))

(check-sat)
(get-model)
