(set-logic ALL)
; Constraint ID: 76d21c6f4a9cb013
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60289)) (False)
(assert (not (not (= x 60289))))

(check-sat)
(get-model)
