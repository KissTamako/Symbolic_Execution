(set-logic ALL)
; Constraint ID: e89fdaae623c1d4a
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60361)) (False)
(assert (not (not (= x 60361))))

(check-sat)
(get-model)
