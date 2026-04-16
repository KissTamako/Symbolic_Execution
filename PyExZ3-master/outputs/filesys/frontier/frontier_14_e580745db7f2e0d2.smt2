(set-logic ALL)
; Frontier Constraint ID: e580745db7f2e0d2
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1633)) (False)
(assert (not (not (= x 1633))))

(check-sat)
(get-model)
