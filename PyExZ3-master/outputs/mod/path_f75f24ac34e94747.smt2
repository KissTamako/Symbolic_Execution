(set-logic ALL)
; Path ID: f75f24ac34e94747
; Generated at: 2026-04-16 12:01:30
; Solver: Z3Wrapper
; Number of assertions: 2
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((< y 10)) (True)
(assert (< y 10))
; ((> y 0)) (True)
(assert (> y 0))

; Query: ((== (% x (+ y 1)) 3)) (True)
(assert (not (= % 3)))

(check-sat)
(get-model)
