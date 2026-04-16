(set-logic ALL)
; Frontier Constraint ID: 5211da224d65f912
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2521)) (False)
(assert (not (= x 2521)))

; Query: ((== x 2522)) (False)
(assert (not (not (= x 2522))))

(check-sat)
(get-model)
