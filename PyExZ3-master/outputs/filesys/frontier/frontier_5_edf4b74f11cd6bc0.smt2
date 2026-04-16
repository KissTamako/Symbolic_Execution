(set-logic ALL)
; Frontier Constraint ID: edf4b74f11cd6bc0
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1693)) (False)
(assert (not (= x 1693)))

; Query: ((== x 1694)) (False)
(assert (not (not (= x 1694))))

(check-sat)
(get-model)
