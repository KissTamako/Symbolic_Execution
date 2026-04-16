(set-logic ALL)
; Constraint ID: fd1c3d675dd74d9f
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59698)) (False)
(assert (not (= x 59698)))

; Query: ((== x 59699)) (False)
(assert (not (not (= x 59699))))

(check-sat)
(get-model)
