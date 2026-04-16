(set-logic ALL)
; Frontier Constraint ID: 050303c23b116631
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1186)) (False)
(assert (not (= x 1186)))

; Query: ((== x 1187)) (False)
(assert (not (not (= x 1187))))

(check-sat)
(get-model)
