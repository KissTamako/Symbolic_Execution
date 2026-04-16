(set-logic ALL)
; Frontier Constraint ID: 38b0631bb6e745a8
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 874)) (False)
(assert (not (not (= x 874))))

(check-sat)
(get-model)
