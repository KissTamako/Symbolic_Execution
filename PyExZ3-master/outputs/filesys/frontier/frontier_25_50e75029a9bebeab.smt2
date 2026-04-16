(set-logic ALL)
; Frontier Constraint ID: 50e75029a9bebeab
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 673)) (False)
(assert (not (= x 673)))

; Query: ((== x 674)) (False)
(assert (not (not (= x 674))))

(check-sat)
(get-model)
