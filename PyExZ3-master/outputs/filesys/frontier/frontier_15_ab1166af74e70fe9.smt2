(set-logic ALL)
; Frontier Constraint ID: ab1166af74e70fe9
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2533)) (False)
(assert (not (= x 2533)))

; Query: ((== x 2534)) (False)
(assert (not (not (= x 2534))))

(check-sat)
(get-model)
