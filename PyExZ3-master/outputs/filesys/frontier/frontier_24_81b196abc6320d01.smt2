(set-logic ALL)
; Constraint ID: 81b196abc6320d01
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60547)) (False)
(assert (not (not (= x 60547))))

(check-sat)
(get-model)
