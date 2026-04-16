(set-logic ALL)
; Constraint ID: 2b22a0b0130d2df1
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59482)) (False)
(assert (not (not (= x 59482))))

(check-sat)
(get-model)
