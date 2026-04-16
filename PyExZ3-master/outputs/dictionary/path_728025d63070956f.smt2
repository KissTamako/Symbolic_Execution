(set-logic ALL)
; Path ID: 728025d63070956f
; Generated at: 2026-04-16 12:01:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const in1 Int)
(declare-const se Int)


; Query: ((== in1 3)) (True)
(assert (not (= in1 3)))

(check-sat)
(get-model)
