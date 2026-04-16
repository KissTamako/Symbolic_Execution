(set-logic ALL)
; Frontier Constraint ID: 62d52cdc185185db
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1870)) (False)
(assert (not (not (= x 1870))))

(check-sat)
(get-model)
