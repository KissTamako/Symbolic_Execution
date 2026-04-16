(set-logic ALL)
; Frontier Constraint ID: 0ef636ee02e210b8
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 496)) (False)
(assert (not (= x 496)))

; Query: ((== x 497)) (False)
(assert (not (not (= x 497))))

(check-sat)
(get-model)
