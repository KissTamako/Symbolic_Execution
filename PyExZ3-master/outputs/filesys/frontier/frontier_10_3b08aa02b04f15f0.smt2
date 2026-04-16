(set-logic ALL)
; Constraint ID: 3b08aa02b04f15f0
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60001)) (False)
(assert (not (not (= x 60001))))

(check-sat)
(get-model)
