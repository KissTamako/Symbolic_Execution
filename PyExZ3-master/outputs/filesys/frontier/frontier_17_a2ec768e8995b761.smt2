(set-logic ALL)
; Frontier Constraint ID: a2ec768e8995b761
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 586)) (False)
(assert (not (= x 586)))

; Query: ((== x 587)) (False)
(assert (not (not (= x 587))))

(check-sat)
(get-model)
