(set-logic ALL)
; Constraint ID: b4dc47fb5629271b
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59464)) (False)
(assert (not (= x 59464)))

; Query: ((== x 59465)) (False)
(assert (not (not (= x 59465))))

(check-sat)
(get-model)
