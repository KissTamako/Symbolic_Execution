(set-logic ALL)
; Frontier Constraint ID: ba3c2e5a4ae26f2b
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 583)) (False)
(assert (not (not (= x 583))))

(check-sat)
(get-model)
