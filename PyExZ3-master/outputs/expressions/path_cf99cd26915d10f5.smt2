(set-logic ALL)
; Path ID: cf99cd26915d10f5
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const se Int)


; Query: ((== (* in1 (+ in2 47)) 53)) (True)
(assert (not (= (* in1 (+ in2 47)) 53)))

(check-sat)
(get-model)
