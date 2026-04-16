(set-logic ALL)
; Frontier Constraint ID: ecf43a6cbab8a39b
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 421)) (False)
(assert (not (= x 421)))

; Query: ((== x 422)) (False)
(assert (not (not (= x 422))))

(check-sat)
(get-model)
