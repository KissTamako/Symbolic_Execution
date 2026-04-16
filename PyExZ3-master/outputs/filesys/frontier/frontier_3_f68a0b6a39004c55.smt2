(set-logic ALL)
; Constraint ID: f68a0b6a39004c55
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59839)) (False)
(assert (not (= x 59839)))

; Query: ((== x 59840)) (False)
(assert (not (not (= x 59840))))

(check-sat)
(get-model)
