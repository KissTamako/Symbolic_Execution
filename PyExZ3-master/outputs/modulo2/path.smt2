(set-logic ALL)
; Path ID: 77dbeb9ecc0aff78
; Generated at: 2026-04-16 12:01:30
; Solver: Z3Wrapper
; Number of assertions: 2
; Has query: True

(declare-const in1 Int)
(declare-const se Int)

; ((!= (% in1 3) 0)) (False)
(assert (not (not (= % 0))))
; ((<= in1 0)) (False)
(assert (not (<= in1 0)))

; Query: ((!= (% in1 5) 0)) (False)
(assert (not (not (not (= % 0)))))

(check-sat)
(get-model)
