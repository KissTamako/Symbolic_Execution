(set-logic ALL)
; Frontier Constraint ID: e11a3a5402f68222
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 373)) (False)
(assert (not (= x 373)))

; Query: ((== x 374)) (False)
(assert (not (not (= x 374))))

(check-sat)
(get-model)
