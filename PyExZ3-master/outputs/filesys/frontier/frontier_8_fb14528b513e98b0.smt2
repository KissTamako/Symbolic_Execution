(set-logic ALL)
; Frontier Constraint ID: fb14528b513e98b0
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 349)) (False)
(assert (not (not (= x 349))))

(check-sat)
(get-model)
