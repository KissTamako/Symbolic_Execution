(set-logic ALL)
; Frontier Constraint ID: bfdbbffafc3f251a
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2827)) (False)
(assert (not (= x 2827)))

; Query: ((== x 2828)) (False)
(assert (not (not (= x 2828))))

(check-sat)
(get-model)
