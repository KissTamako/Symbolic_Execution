(set-logic ALL)
; Frontier Constraint ID: a62311ffe9088046
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2437)) (False)
(assert (not (not (= x 2437))))

(check-sat)
(get-model)
