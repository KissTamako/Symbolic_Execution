(set-logic ALL)
; Frontier Constraint ID: 434c6722eca20aab
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 889)) (False)
(assert (not (= x 889)))

; Query: ((== x 890)) (False)
(assert (not (not (= x 890))))

(check-sat)
(get-model)
