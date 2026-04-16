(set-logic ALL)
; Frontier Constraint ID: 60fdabcbd20efbc0
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 361)) (False)
(assert (not (= x 361)))

; Query: ((== x 362)) (False)
(assert (not (not (= x 362))))

(check-sat)
(get-model)
