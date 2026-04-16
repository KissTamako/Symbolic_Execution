(set-logic ALL)
; Constraint ID: b89c2dde32d4e32c
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59569)) (False)
(assert (not (= x 59569)))

; Query: ((== x 59570)) (False)
(assert (not (not (= x 59570))))

(check-sat)
(get-model)
