(set-logic ALL)
; Constraint ID: ed0cb82a94737803
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60151)) (False)
(assert (not (= x 60151)))

; Query: ((== x 60152)) (False)
(assert (not (not (= x 60152))))

(check-sat)
(get-model)
