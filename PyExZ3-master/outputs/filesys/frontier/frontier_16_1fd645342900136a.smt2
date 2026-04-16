(set-logic ALL)
; Constraint ID: 1fd645342900136a
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60610)) (False)
(assert (not (not (= x 60610))))

(check-sat)
(get-model)
