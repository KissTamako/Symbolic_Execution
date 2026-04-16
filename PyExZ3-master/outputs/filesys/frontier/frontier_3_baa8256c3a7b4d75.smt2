(set-logic ALL)
; Frontier Constraint ID: baa8256c3a7b4d75
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 865)) (False)
(assert (not (= x 865)))

; Query: ((== x 866)) (False)
(assert (not (not (= x 866))))

(check-sat)
(get-model)
