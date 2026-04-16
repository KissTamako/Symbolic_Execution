(set-logic ALL)
; Frontier Constraint ID: 08d8bf2dc17d2541
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 739)) (False)
(assert (not (not (= x 739))))

(check-sat)
(get-model)
