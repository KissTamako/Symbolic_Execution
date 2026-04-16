(set-logic ALL)
; Constraint ID: dc12eeb75194112e
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59272)) (False)
(assert (not (= x 59272)))

; Query: ((== x 59273)) (False)
(assert (not (not (= x 59273))))

(check-sat)
(get-model)
