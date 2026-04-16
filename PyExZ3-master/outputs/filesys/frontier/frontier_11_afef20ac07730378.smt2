(set-logic ALL)
; Constraint ID: afef20ac07730378
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59326)) (False)
(assert (not (= x 59326)))

; Query: ((== x 59327)) (False)
(assert (not (not (= x 59327))))

(check-sat)
(get-model)
