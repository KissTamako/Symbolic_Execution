(set-logic ALL)
; Constraint ID: 85aec102f8c80c6b
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60613)) (False)
(assert (not (not (= x 60613))))

(check-sat)
(get-model)
