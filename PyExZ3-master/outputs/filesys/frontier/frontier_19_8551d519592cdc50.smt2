(set-logic ALL)
; Frontier Constraint ID: 8551d519592cdc50
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 364)) (False)
(assert (not (= x 364)))

; Query: ((== x 365)) (False)
(assert (not (not (= x 365))))

(check-sat)
(get-model)
