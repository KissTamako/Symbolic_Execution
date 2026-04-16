(set-logic ALL)
; Frontier Constraint ID: 24bed87b20d3bc6d
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1036)) (False)
(assert (not (= x 1036)))

; Query: ((== x 1037)) (False)
(assert (not (not (= x 1037))))

(check-sat)
(get-model)
