(set-logic ALL)
; Constraint ID: af3baf46288ca551
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60586)) (False)
(assert (not (not (= x 60586))))

(check-sat)
(get-model)
