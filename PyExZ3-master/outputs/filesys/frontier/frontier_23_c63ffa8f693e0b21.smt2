(set-logic ALL)
; Frontier Constraint ID: c63ffa8f693e0b21
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1720)) (False)
(assert (not (= x 1720)))

; Query: ((== x 1721)) (False)
(assert (not (not (= x 1721))))

(check-sat)
(get-model)
