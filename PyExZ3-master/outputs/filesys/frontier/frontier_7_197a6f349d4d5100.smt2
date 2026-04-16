(set-logic ALL)
; Frontier Constraint ID: 197a6f349d4d5100
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 646)) (False)
(assert (not (= x 646)))

; Query: ((== x 647)) (False)
(assert (not (not (= x 647))))

(check-sat)
(get-model)
