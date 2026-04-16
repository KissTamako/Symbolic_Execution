(set-logic ALL)
; Frontier Constraint ID: 1c48ecb65daa9cf3
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 742)) (False)
(assert (not (= x 742)))

; Query: ((== x 743)) (False)
(assert (not (not (= x 743))))

(check-sat)
(get-model)
