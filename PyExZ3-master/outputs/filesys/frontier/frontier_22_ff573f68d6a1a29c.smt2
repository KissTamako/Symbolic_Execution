(set-logic ALL)
; Frontier Constraint ID: ff573f68d6a1a29c
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 595)) (False)
(assert (not (not (= x 595))))

(check-sat)
(get-model)
