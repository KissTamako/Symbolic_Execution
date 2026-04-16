(set-logic ALL)
; Constraint ID: 9a0701264ce957bd
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60373)) (False)
(assert (not (not (= x 60373))))

(check-sat)
(get-model)
