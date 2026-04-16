(set-logic ALL)
; Frontier Constraint ID: 75a7e7f1d8e76851
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 415)) (False)
(assert (not (not (= x 415))))

(check-sat)
(get-model)
