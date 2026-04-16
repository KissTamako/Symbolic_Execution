(set-logic ALL)
; Frontier Constraint ID: dd4e93255c3736ab
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2548)) (False)
(assert (not (= x 2548)))

; Query: ((== x 2549)) (False)
(assert (not (not (= x 2549))))

(check-sat)
(get-model)
