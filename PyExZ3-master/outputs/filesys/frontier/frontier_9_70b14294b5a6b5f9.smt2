(set-logic ALL)
; Frontier Constraint ID: 70b14294b5a6b5f9
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 424)) (False)
(assert (not (= x 424)))

; Query: ((== x 425)) (False)
(assert (not (not (= x 425))))

(check-sat)
(get-model)
