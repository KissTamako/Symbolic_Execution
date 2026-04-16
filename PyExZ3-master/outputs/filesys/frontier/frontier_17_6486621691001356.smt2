(set-logic ALL)
; Frontier Constraint ID: 6486621691001356
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1486)) (False)
(assert (not (= x 1486)))

; Query: ((== x 1487)) (False)
(assert (not (not (= x 1487))))

(check-sat)
(get-model)
