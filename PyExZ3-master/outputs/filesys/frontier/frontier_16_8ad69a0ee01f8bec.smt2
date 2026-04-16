(set-logic ALL)
; Frontier Constraint ID: 8ad69a0ee01f8bec
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1636)) (False)
(assert (not (not (= x 1636))))

(check-sat)
(get-model)
