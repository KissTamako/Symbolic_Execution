(set-logic ALL)
; Frontier Constraint ID: a5306625fbdc42cd
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 649)) (False)
(assert (not (not (= x 649))))

(check-sat)
(get-model)
