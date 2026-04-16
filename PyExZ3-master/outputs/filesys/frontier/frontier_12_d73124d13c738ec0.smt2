(set-logic ALL)
; Constraint ID: d73124d13c738ec0
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60079)) (False)
(assert (not (not (= x 60079))))

(check-sat)
(get-model)
