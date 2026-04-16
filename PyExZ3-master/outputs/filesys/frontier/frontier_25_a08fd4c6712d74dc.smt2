(set-logic ALL)
; Constraint ID: a08fd4c6712d74dc
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59422)) (False)
(assert (not (= x 59422)))

; Query: ((== x 59423)) (False)
(assert (not (not (= x 59423))))

(check-sat)
(get-model)
