(set-logic ALL)
; Frontier Constraint ID: 1c955314355c4677
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 745)) (False)
(assert (not (= x 745)))

; Query: ((== x 746)) (False)
(assert (not (not (= x 746))))

(check-sat)
(get-model)
