(set-logic ALL)
; Constraint ID: a0a77d845ed21523
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59248)) (False)
(assert (not (not (= x 59248))))

(check-sat)
(get-model)
