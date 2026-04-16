(set-logic ALL)
; Path ID: 3b316710c3fc94de
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59311)) (False)
(assert (not (not (= x 59311))))

(check-sat)
(get-model)
