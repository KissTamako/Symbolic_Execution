(set-logic ALL)
; Path ID: 0ef010d1760e8cd8
; Generated at: 2026-04-16 12:01:20
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)
(declare-const y Int)

; ((>= y 4294967296)) (True)
(assert (>= y 4294967296))

; Query: ((== x 4294967296)) (False)
(assert (not (not (= x 4294967296))))

(check-sat)
(get-model)
