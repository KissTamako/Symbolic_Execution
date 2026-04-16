(set-logic ALL)
; Constraint ID: bbe7dff881b034e9
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59335)) (False)
(assert (not (= x 59335)))

; Query: ((== x 59336)) (False)
(assert (not (not (= x 59336))))

(check-sat)
(get-model)
