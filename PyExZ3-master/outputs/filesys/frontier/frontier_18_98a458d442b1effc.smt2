(set-logic ALL)
; Frontier Constraint ID: 98a458d442b1effc
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1714)) (False)
(assert (not (not (= x 1714))))

(check-sat)
(get-model)
