(set-logic ALL)
; Path ID: 65efadce25c0bca9
; Generated at: 2026-04-16 12:01:31
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const in1 Int)
(declare-const se Int)

; ((== (* in1 in1) 0)) (False)
(assert (not (= (* in1 in1) 0)))

; Query: ((> (* in1 in1) 0)) (True)
(assert (not (> (* in1 in1) 0)))

(check-sat)
(get-model)
