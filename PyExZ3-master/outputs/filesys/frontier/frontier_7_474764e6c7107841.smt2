(set-logic ALL)
; Frontier Constraint ID: 474764e6c7107841
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1471)) (False)
(assert (not (= x 1471)))

; Query: ((== x 1472)) (False)
(assert (not (not (= x 1472))))

(check-sat)
(get-model)
