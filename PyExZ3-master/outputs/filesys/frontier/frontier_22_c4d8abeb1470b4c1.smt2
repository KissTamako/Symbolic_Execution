(set-logic ALL)
; Constraint ID: c4d8abeb1470b4c1
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60319)) (False)
(assert (not (not (= x 60319))))

(check-sat)
(get-model)
