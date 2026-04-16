(set-logic ALL)
; Executed Path ID: 747e4c4f2524d488
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 598)) (False)
(assert (not (= x 598)))
; ((== x 599)) (False)
(assert (not (= x 599)))

(check-sat)
(get-model)
