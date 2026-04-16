(set-logic ALL)
; Constraint ID: 28ed3fd483710eb4
; Generated at: 2026-04-16 10:43:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59470)) (False)
(assert (not (= x 59470)))

; Query: ((== x 59471)) (False)
(assert (not (not (= x 59471))))

(check-sat)
(get-model)
