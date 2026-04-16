(set-logic ALL)
; Constraint ID: bf15b78b18924726
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59722)) (False)
(assert (not (= x 59722)))

; Query: ((== x 59723)) (False)
(assert (not (not (= x 59723))))

(check-sat)
(get-model)
