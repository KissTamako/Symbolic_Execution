(set-logic ALL)
; Constraint ID: 17893828eb1b2ce3
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59989)) (False)
(assert (not (not (= x 59989))))

(check-sat)
(get-model)
