(set-logic ALL)
; Frontier Constraint ID: fa771bd7b5d91a00
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 352)) (False)
(assert (not (not (= x 352))))

(check-sat)
(get-model)
