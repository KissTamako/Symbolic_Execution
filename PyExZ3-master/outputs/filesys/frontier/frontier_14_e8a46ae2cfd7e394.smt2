(set-logic ALL)
; Frontier Constraint ID: e8a46ae2cfd7e394
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1858)) (False)
(assert (not (not (= x 1858))))

(check-sat)
(get-model)
