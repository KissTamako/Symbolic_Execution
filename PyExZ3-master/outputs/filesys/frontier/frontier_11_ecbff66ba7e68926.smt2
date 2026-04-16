(set-logic ALL)
; Frontier Constraint ID: ecbff66ba7e68926
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 577)) (False)
(assert (not (= x 577)))

; Query: ((== x 578)) (False)
(assert (not (not (= x 578))))

(check-sat)
(get-model)
