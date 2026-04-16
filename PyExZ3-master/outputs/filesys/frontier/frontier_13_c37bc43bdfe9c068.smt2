(set-logic ALL)
; Constraint ID: c37bc43bdfe9c068
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59254)) (False)
(assert (not (= x 59254)))

; Query: ((== x 59255)) (False)
(assert (not (not (= x 59255))))

(check-sat)
(get-model)
