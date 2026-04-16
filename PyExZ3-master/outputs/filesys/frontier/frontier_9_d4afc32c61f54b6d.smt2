(set-logic ALL)
; Constraint ID: d4afc32c61f54b6d
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59248)) (False)
(assert (not (= x 59248)))

; Query: ((== x 59249)) (False)
(assert (not (not (= x 59249))))

(check-sat)
(get-model)
