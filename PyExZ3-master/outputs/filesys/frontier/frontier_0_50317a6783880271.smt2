(set-logic ALL)
; Frontier Constraint ID: 50317a6783880271
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1162)) (False)
(assert (not (not (= x 1162))))

(check-sat)
(get-model)
