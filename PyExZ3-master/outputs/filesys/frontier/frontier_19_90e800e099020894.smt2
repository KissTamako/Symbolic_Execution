(set-logic ALL)
; Frontier Constraint ID: 90e800e099020894
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1489)) (False)
(assert (not (= x 1489)))

; Query: ((== x 1490)) (False)
(assert (not (not (= x 1490))))

(check-sat)
(get-model)
