(set-logic ALL)
; Frontier Constraint ID: 4a1deec0528e67fe
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2845)) (False)
(assert (not (= x 2845)))

; Query: ((== x 2846)) (False)
(assert (not (not (= x 2846))))

(check-sat)
(get-model)
