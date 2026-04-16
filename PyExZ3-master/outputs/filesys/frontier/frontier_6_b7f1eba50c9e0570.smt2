(set-logic ALL)
; Constraint ID: b7f1eba50c9e0570
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59995)) (False)
(assert (not (not (= x 59995))))

(check-sat)
(get-model)
