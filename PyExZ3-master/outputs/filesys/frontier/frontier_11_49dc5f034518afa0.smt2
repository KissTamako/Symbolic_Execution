(set-logic ALL)
; Frontier Constraint ID: 49dc5f034518afa0
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2527)) (False)
(assert (not (= x 2527)))

; Query: ((== x 2528)) (False)
(assert (not (not (= x 2528))))

(check-sat)
(get-model)
