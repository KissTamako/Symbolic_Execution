(set-logic ALL)
; Constraint ID: a4d900a422c940b7
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60535)) (False)
(assert (not (= x 60535)))

; Query: ((== x 60536)) (False)
(assert (not (not (= x 60536))))

(check-sat)
(get-model)
