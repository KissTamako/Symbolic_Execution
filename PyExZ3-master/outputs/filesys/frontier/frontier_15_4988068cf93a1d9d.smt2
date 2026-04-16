(set-logic ALL)
; Frontier Constraint ID: 4988068cf93a1d9d
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 583)) (False)
(assert (not (= x 583)))

; Query: ((== x 584)) (False)
(assert (not (not (= x 584))))

(check-sat)
(get-model)
