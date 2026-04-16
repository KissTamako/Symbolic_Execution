(set-logic ALL)
; Frontier Constraint ID: e9f7ec1d9194289a
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 883)) (False)
(assert (not (= x 883)))

; Query: ((== x 884)) (False)
(assert (not (not (= x 884))))

(check-sat)
(get-model)
