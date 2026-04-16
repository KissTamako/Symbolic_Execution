(set-logic ALL)
; Frontier Constraint ID: 322584455b95c37f
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1162)) (False)
(assert (not (= x 1162)))

; Query: ((== x 1163)) (False)
(assert (not (not (= x 1163))))

(check-sat)
(get-model)
