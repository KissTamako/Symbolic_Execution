(set-logic ALL)
; Path ID: 83760c9123807ffd
; Generated at: 2026-04-16 12:01:30
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const i Int)
(declare-const se Int)


; Query: ((> (+ (* 3 (// i 100)) 100) 43)) (False)
(assert (not (not (> (+ (* 3 //) 100) 43))))

(check-sat)
(get-model)
