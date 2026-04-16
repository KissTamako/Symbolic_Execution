(set-logic ALL)
; Constraint ID: d729523bb13e1c37
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59623)) (False)
(assert (not (not (= x 59623))))

(check-sat)
(get-model)
