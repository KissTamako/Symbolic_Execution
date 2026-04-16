(set-logic ALL)
; Constraint ID: c2b7dad6fe154935
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60529)) (False)
(assert (not (not (= x 60529))))

(check-sat)
(get-model)
