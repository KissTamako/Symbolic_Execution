(set-logic ALL)
; Constraint ID: 20cb1e384a01e4e1
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60310)) (False)
(assert (not (not (= x 60310))))

(check-sat)
(get-model)
