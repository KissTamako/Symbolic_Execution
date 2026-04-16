(set-logic ALL)
; Frontier Constraint ID: add54d771addf9fe
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1837)) (False)
(assert (not (= x 1837)))

; Query: ((== x 1838)) (False)
(assert (not (not (= x 1838))))

(check-sat)
(get-model)
