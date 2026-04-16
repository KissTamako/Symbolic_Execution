(set-logic ALL)
; Frontier Constraint ID: 19ff32e32669d64f
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1696)) (False)
(assert (not (= x 1696)))

; Query: ((== x 1697)) (False)
(assert (not (not (= x 1697))))

(check-sat)
(get-model)
