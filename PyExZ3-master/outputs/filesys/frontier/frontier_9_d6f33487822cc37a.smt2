(set-logic ALL)
; Frontier Constraint ID: d6f33487822cc37a
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 724)) (False)
(assert (not (= x 724)))

; Query: ((== x 725)) (False)
(assert (not (not (= x 725))))

(check-sat)
(get-model)
