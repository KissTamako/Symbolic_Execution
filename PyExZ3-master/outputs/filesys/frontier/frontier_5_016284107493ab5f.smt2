(set-logic ALL)
; Frontier Constraint ID: 016284107493ab5f
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 568)) (False)
(assert (not (= x 568)))

; Query: ((== x 569)) (False)
(assert (not (not (= x 569))))

(check-sat)
(get-model)
