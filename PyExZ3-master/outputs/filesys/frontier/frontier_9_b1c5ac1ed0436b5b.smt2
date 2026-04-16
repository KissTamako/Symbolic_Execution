(set-logic ALL)
; Constraint ID: b1c5ac1ed0436b5b
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59998)) (False)
(assert (not (= x 59998)))

; Query: ((== x 59999)) (False)
(assert (not (not (= x 59999))))

(check-sat)
(get-model)
