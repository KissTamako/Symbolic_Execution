(set-logic ALL)
; Constraint ID: 19b58a13155667fa
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59695)) (False)
(assert (not (= x 59695)))

; Query: ((== x 59696)) (False)
(assert (not (not (= x 59696))))

(check-sat)
(get-model)
