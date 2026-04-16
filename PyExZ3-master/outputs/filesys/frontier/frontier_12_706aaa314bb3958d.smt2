(set-logic ALL)
; Frontier Constraint ID: 706aaa314bb3958d
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1855)) (False)
(assert (not (not (= x 1855))))

(check-sat)
(get-model)
