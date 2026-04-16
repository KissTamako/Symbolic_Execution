(set-logic ALL)
; Constraint ID: 53b144ff80d33a97
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59497)) (False)
(assert (not (= x 59497)))

; Query: ((== x 59498)) (False)
(assert (not (not (= x 59498))))

(check-sat)
(get-model)
