(set-logic ALL)
; Constraint ID: 59336c5621723342
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60604)) (False)
(assert (not (= x 60604)))

; Query: ((== x 60605)) (False)
(assert (not (not (= x 60605))))

(check-sat)
(get-model)
