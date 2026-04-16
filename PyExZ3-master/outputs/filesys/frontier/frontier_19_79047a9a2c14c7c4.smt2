(set-logic ALL)
; Frontier Constraint ID: 79047a9a2c14c7c4
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 514)) (False)
(assert (not (= x 514)))

; Query: ((== x 515)) (False)
(assert (not (not (= x 515))))

(check-sat)
(get-model)
