(set-logic ALL)
; Constraint ID: 1cea126941dc2d0f
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60304)) (False)
(assert (not (not (= x 60304))))

(check-sat)
(get-model)
