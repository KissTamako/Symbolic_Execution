(set-logic ALL)
; Constraint ID: 4690bbfb03c5cd56
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59347)) (False)
(assert (not (= x 59347)))

; Query: ((== x 59348)) (False)
(assert (not (not (= x 59348))))

(check-sat)
(get-model)
