(set-logic ALL)
; Constraint ID: 247eab2173f7554d
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60382)) (False)
(assert (not (not (= x 60382))))

(check-sat)
(get-model)
