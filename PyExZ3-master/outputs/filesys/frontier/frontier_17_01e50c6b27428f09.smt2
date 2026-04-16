(set-logic ALL)
; Frontier Constraint ID: 01e50c6b27428f09
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 886)) (False)
(assert (not (= x 886)))

; Query: ((== x 887)) (False)
(assert (not (not (= x 887))))

(check-sat)
(get-model)
