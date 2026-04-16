(set-logic ALL)
; Constraint ID: 88d8e5584785dad2
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60292)) (False)
(assert (not (not (= x 60292))))

(check-sat)
(get-model)
