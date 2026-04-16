(set-logic ALL)
; Frontier Constraint ID: 9b8ecdf38ea8a10c
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1021)) (False)
(assert (not (not (= x 1021))))

(check-sat)
(get-model)
