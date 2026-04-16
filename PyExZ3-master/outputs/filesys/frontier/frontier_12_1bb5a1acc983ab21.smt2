(set-logic ALL)
; Frontier Constraint ID: 1bb5a1acc983ab21
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 430)) (False)
(assert (not (not (= x 430))))

(check-sat)
(get-model)
