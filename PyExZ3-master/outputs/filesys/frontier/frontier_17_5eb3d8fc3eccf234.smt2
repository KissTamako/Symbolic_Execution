(set-logic ALL)
; Frontier Constraint ID: 5eb3d8fc3eccf234
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1711)) (False)
(assert (not (= x 1711)))

; Query: ((== x 1712)) (False)
(assert (not (not (= x 1712))))

(check-sat)
(get-model)
