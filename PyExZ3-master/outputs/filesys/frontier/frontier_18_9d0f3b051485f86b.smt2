(set-logic ALL)
; Constraint ID: 9d0f3b051485f86b
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60463)) (False)
(assert (not (not (= x 60463))))

(check-sat)
(get-model)
