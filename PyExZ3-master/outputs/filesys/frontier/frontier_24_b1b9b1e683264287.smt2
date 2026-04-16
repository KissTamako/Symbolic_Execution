(set-logic ALL)
; Constraint ID: b1b9b1e683264287
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60472)) (False)
(assert (not (not (= x 60472))))

(check-sat)
(get-model)
