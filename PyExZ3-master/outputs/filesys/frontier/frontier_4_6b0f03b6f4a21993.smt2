(set-logic ALL)
; Frontier Constraint ID: 6b0f03b6f4a21993
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1843)) (False)
(assert (not (not (= x 1843))))

(check-sat)
(get-model)
