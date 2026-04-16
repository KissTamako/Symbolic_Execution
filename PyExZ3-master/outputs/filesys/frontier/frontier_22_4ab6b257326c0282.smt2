(set-logic ALL)
; Constraint ID: 4ab6b257326c0282
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60544)) (False)
(assert (not (not (= x 60544))))

(check-sat)
(get-model)
