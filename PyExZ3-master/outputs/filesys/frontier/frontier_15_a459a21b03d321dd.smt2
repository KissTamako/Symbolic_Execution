(set-logic ALL)
; Frontier Constraint ID: a459a21b03d321dd
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1483)) (False)
(assert (not (= x 1483)))

; Query: ((== x 1484)) (False)
(assert (not (not (= x 1484))))

(check-sat)
(get-model)
