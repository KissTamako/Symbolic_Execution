(set-logic ALL)
; Frontier Constraint ID: f22b867fac5be9cc
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1348)) (False)
(assert (not (= x 1348)))

; Query: ((== x 1349)) (False)
(assert (not (not (= x 1349))))

(check-sat)
(get-model)
