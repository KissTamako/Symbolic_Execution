(set-logic ALL)
; Frontier Constraint ID: 197bebe1e9b52f10
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1177)) (False)
(assert (not (= x 1177)))

; Query: ((== x 1178)) (False)
(assert (not (not (= x 1178))))

(check-sat)
(get-model)
