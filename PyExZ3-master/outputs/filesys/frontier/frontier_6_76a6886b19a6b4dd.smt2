(set-logic ALL)
; Constraint ID: 76a6886b19a6b4dd
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60295)) (False)
(assert (not (not (= x 60295))))

(check-sat)
(get-model)
