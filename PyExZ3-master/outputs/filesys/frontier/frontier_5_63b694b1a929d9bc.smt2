(set-logic ALL)
; Frontier Constraint ID: 63b694b1a929d9bc
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 643)) (False)
(assert (not (= x 643)))

; Query: ((== x 644)) (False)
(assert (not (not (= x 644))))

(check-sat)
(get-model)
