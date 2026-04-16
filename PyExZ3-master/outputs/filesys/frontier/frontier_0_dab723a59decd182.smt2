(set-logic ALL)
; Frontier Constraint ID: dab723a59decd182
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2812)) (False)
(assert (not (not (= x 2812))))

(check-sat)
(get-model)
