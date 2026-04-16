(set-logic ALL)
; Constraint ID: 5c105035e5a33bee
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60376)) (False)
(assert (not (not (= x 60376))))

(check-sat)
(get-model)
