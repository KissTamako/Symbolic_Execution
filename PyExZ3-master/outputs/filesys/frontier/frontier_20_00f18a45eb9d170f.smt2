(set-logic ALL)
; Frontier Constraint ID: 00f18a45eb9d170f
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1867)) (False)
(assert (not (not (= x 1867))))

(check-sat)
(get-model)
