(set-logic ALL)
; Constraint ID: d02b0322bce6718c
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59914)) (False)
(assert (not (not (= x 59914))))

(check-sat)
(get-model)
