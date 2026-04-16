(set-logic ALL)
; Frontier Constraint ID: 69534d3ce8034fd2
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1012)) (False)
(assert (not (= x 1012)))

; Query: ((== x 1013)) (False)
(assert (not (not (= x 1013))))

(check-sat)
(get-model)
