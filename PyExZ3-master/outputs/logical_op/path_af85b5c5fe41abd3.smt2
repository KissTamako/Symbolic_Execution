(set-logic ALL)
; Path ID: af85b5c5fe41abd3
; Generated at: 2026-04-16 12:01:29
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const in1 Int)
(declare-const in2 Int)
(declare-const se Int)

; ((== (& in1 in2) 1)) (True)
(assert (= & 1))

; Query: ((== (& in1 in2) 7)) (False)
(assert (not (not (= & 7))))

(check-sat)
(get-model)
