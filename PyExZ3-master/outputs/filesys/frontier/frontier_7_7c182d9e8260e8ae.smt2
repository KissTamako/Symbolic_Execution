(set-logic ALL)
; Constraint ID: 7c182d9e8260e8ae
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59395)) (False)
(assert (not (= x 59395)))

; Query: ((== x 59396)) (False)
(assert (not (not (= x 59396))))

(check-sat)
(get-model)
