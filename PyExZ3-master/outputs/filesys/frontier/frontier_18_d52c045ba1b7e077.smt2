(set-logic ALL)
; Frontier Constraint ID: d52c045ba1b7e077
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1489)) (False)
(assert (not (not (= x 1489))))

(check-sat)
(get-model)
