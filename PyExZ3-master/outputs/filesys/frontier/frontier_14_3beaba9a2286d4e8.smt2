(set-logic ALL)
; Frontier Constraint ID: 3beaba9a2286d4e8
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 658)) (False)
(assert (not (not (= x 658))))

(check-sat)
(get-model)
