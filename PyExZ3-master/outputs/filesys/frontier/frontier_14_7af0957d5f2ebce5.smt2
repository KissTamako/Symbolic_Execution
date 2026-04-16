(set-logic ALL)
; Constraint ID: 7af0957d5f2ebce5
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60607)) (False)
(assert (not (not (= x 60607))))

(check-sat)
(get-model)
