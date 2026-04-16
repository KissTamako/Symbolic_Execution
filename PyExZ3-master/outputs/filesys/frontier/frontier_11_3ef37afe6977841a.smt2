(set-logic ALL)
; Frontier Constraint ID: 3ef37afe6977841a
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 877)) (False)
(assert (not (= x 877)))

; Query: ((== x 878)) (False)
(assert (not (not (= x 878))))

(check-sat)
(get-model)
