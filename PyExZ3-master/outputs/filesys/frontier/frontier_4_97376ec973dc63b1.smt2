(set-logic ALL)
; Frontier Constraint ID: 97376ec973dc63b1
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 868)) (False)
(assert (not (not (= x 868))))

(check-sat)
(get-model)
