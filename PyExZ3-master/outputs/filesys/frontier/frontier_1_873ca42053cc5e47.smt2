(set-logic ALL)
; Frontier Constraint ID: 873ca42053cc5e47
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 337)) (False)
(assert (not (= x 337)))

; Query: ((== x 338)) (False)
(assert (not (not (= x 338))))

(check-sat)
(get-model)
