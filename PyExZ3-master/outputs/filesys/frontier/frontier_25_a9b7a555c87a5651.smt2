(set-logic ALL)
; Constraint ID: a9b7a555c87a5651
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59647)) (False)
(assert (not (= x 59647)))

; Query: ((== x 59648)) (False)
(assert (not (not (= x 59648))))

(check-sat)
(get-model)
