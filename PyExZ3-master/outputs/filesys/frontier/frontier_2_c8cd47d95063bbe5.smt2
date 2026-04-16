(set-logic ALL)
; Frontier Constraint ID: c8cd47d95063bbe5
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2815)) (False)
(assert (not (not (= x 2815))))

(check-sat)
(get-model)
