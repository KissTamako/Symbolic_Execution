(set-logic ALL)
; Constraint ID: d2c4d6fa828b1718
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59338)) (False)
(assert (not (not (= x 59338))))

(check-sat)
(get-model)
