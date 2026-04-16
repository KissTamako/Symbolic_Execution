(set-logic ALL)
; Frontier Constraint ID: eba05c44bbc72d51
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 598)) (False)
(assert (not (= x 598)))

; Query: ((== x 599)) (False)
(assert (not (not (= x 599))))

(check-sat)
(get-model)
