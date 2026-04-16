(set-logic ALL)
; Frontier Constraint ID: 57b892e313cf7551
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 505)) (False)
(assert (not (not (= x 505))))

(check-sat)
(get-model)
