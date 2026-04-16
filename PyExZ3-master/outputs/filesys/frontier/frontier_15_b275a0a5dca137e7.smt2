(set-logic ALL)
; Constraint ID: b275a0a5dca137e7
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60607)) (False)
(assert (not (= x 60607)))

; Query: ((== x 60608)) (False)
(assert (not (not (= x 60608))))

(check-sat)
(get-model)
