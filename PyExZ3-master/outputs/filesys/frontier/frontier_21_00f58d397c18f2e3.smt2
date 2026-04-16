(set-logic ALL)
; Constraint ID: 00f58d397c18f2e3
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60166)) (False)
(assert (not (= x 60166)))

; Query: ((== x 60167)) (False)
(assert (not (not (= x 60167))))

(check-sat)
(get-model)
