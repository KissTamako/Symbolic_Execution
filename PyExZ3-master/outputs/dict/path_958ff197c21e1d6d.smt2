(set-logic ALL)
; Path ID: 958ff197c21e1d6d
; Generated at: 2026-04-16 12:01:23
; Solver: Z3Wrapper
; Number of assertions: 3
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 1)) (True)
(assert (= x 1))
; ((== x 101)) (False)
(assert (not (= x 101)))
; ((== x 4)) (False)
(assert (not (= x 4)))

; Query: ((== x 1)) (True)
(assert (not (= x 1)))

(check-sat)
(get-model)
