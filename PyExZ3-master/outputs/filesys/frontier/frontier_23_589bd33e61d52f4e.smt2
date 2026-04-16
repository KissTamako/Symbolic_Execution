(set-logic ALL)
; Frontier Constraint ID: 589bd33e61d52f4e
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2545)) (False)
(assert (not (= x 2545)))

; Query: ((== x 2546)) (False)
(assert (not (not (= x 2546))))

(check-sat)
(get-model)
