(set-logic ALL)
; Frontier Constraint ID: 81ad25abb5e4cc50
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1861)) (False)
(assert (not (= x 1861)))

; Query: ((== x 1862)) (False)
(assert (not (not (= x 1862))))

(check-sat)
(get-model)
