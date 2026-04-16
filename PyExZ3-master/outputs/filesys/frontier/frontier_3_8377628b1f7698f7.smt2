(set-logic ALL)
; Frontier Constraint ID: 8377628b1f7698f7
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1465)) (False)
(assert (not (= x 1465)))

; Query: ((== x 1466)) (False)
(assert (not (not (= x 1466))))

(check-sat)
(get-model)
