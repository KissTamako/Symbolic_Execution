(set-logic ALL)
; Constraint ID: 837e8cd409288865
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59992)) (False)
(assert (not (not (= x 59992))))

(check-sat)
(get-model)
