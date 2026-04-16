(set-logic ALL)
; Constraint ID: 056f724f07930908
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59479)) (False)
(assert (not (= x 59479)))

; Query: ((== x 59480)) (False)
(assert (not (not (= x 59480))))

(check-sat)
(get-model)
