(set-logic ALL)
; Frontier Constraint ID: 58cb4ea9e84b4a49
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1042)) (False)
(assert (not (= x 1042)))

; Query: ((== x 1043)) (False)
(assert (not (not (= x 1043))))

(check-sat)
(get-model)
