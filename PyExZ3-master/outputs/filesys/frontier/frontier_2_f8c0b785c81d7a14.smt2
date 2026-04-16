(set-logic ALL)
; Frontier Constraint ID: f8c0b785c81d7a14
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1315)) (False)
(assert (not (not (= x 1315))))

(check-sat)
(get-model)
