(set-logic ALL)
; Frontier Constraint ID: 34c8f5ed3885661e
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2824)) (False)
(assert (not (= x 2824)))

; Query: ((== x 2825)) (False)
(assert (not (not (= x 2825))))

(check-sat)
(get-model)
