(set-logic ALL)
; Path ID: 3cc7eba669cf2c5d
; Generated at: 2026-04-16 12:01:30
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const in1 Int)
(declare-const se Int)

; ((!= (% in1 3) 0)) (False)
(assert (not (not (= % 0))))

; Query: ((!= (% in1 5) 0)) (True)
(assert (not (not (= % 0))))

(check-sat)
(get-model)
