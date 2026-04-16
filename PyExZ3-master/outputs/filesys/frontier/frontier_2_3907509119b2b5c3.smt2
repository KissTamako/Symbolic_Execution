(set-logic ALL)
; Frontier Constraint ID: 3907509119b2b5c3
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 865)) (False)
(assert (not (not (= x 865))))

(check-sat)
(get-model)
