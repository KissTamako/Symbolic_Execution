(set-logic ALL)
; Frontier Constraint ID: f661df4c89b2d120
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1474)) (False)
(assert (not (= x 1474)))

; Query: ((== x 1475)) (False)
(assert (not (not (= x 1475))))

(check-sat)
(get-model)
