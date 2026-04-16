(set-logic ALL)
; Constraint ID: 2dabfbb90114cf87
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60013)) (False)
(assert (not (not (= x 60013))))

(check-sat)
(get-model)
