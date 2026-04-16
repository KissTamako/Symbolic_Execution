(set-logic ALL)
; Frontier Constraint ID: 090ed2f8a4aa5693
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1645)) (False)
(assert (not (= x 1645)))

; Query: ((== x 1646)) (False)
(assert (not (not (= x 1646))))

(check-sat)
(get-model)
