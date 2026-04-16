(set-logic ALL)
; Frontier Constraint ID: b93ce9c074040f3e
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 430)) (False)
(assert (not (= x 430)))

; Query: ((== x 431)) (False)
(assert (not (not (= x 431))))

(check-sat)
(get-model)
