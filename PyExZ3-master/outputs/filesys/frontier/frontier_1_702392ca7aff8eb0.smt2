(set-logic ALL)
; Frontier Constraint ID: 702392ca7aff8eb0
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2512)) (False)
(assert (not (= x 2512)))

; Query: ((== x 2513)) (False)
(assert (not (not (= x 2513))))

(check-sat)
(get-model)
