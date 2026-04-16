(set-logic ALL)
; Path ID: 894ac1b1579bc8bb
; Generated at: 2026-04-16 12:01:32
; Solver: Z3Wrapper
; Number of assertions: 5
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 12)) (False)
(assert (not (= x 12)))
; ((== x 9)) (False)
(assert (not (= x 9)))
; ((== x 19)) (False)
(assert (not (= x 19)))
; ((== x 3)) (False)
(assert (not (= x 3)))
; ((== x 1)) (False)
(assert (not (= x 1)))

; Query: ((== x 15)) (True)
(assert (not (= x 15)))

(check-sat)
(get-model)
