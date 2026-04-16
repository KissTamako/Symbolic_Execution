(set-logic ALL)
; Constraint ID: 6a1623e5d129e406
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60541)) (False)
(assert (not (not (= x 60541))))

(check-sat)
(get-model)
