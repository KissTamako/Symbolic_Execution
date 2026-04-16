(set-logic ALL)
; Frontier Constraint ID: f7baa526c190cd5b
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2836)) (False)
(assert (not (= x 2836)))

; Query: ((== x 2837)) (False)
(assert (not (not (= x 2837))))

(check-sat)
(get-model)
