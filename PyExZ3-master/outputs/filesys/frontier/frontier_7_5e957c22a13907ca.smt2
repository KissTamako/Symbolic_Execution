(set-logic ALL)
; Frontier Constraint ID: 5e957c22a13907ca
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 571)) (False)
(assert (not (= x 571)))

; Query: ((== x 572)) (False)
(assert (not (not (= x 572))))

(check-sat)
(get-model)
