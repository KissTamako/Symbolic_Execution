(set-logic ALL)
; Frontier Constraint ID: d5678356edeb7908
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 574)) (False)
(assert (not (= x 574)))

; Query: ((== x 575)) (False)
(assert (not (not (= x 575))))

(check-sat)
(get-model)
