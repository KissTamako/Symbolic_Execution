(set-logic ALL)
; Constraint ID: 4d2daeb6af2c9da3
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59614)) (False)
(assert (not (= x 59614)))

; Query: ((== x 59615)) (False)
(assert (not (not (= x 59615))))

(check-sat)
(get-model)
