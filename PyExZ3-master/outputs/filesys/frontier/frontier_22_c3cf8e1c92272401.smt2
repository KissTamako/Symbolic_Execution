(set-logic ALL)
; Constraint ID: c3cf8e1c92272401
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60244)) (False)
(assert (not (not (= x 60244))))

(check-sat)
(get-model)
