(set-logic ALL)
; Frontier Constraint ID: 63ab224d0fdeb930
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 730)) (False)
(assert (not (= x 730)))

; Query: ((== x 731)) (False)
(assert (not (not (= x 731))))

(check-sat)
(get-model)
