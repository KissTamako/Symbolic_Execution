(set-logic ALL)
; Constraint ID: 0bf57d8a3876d6ab
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60532)) (False)
(assert (not (= x 60532)))

; Query: ((== x 60533)) (False)
(assert (not (not (= x 60533))))

(check-sat)
(get-model)
