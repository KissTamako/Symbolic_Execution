(set-logic ALL)
; Constraint ID: f4e86a8d60a8e55f
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60088)) (False)
(assert (not (not (= x 60088))))

(check-sat)
(get-model)
