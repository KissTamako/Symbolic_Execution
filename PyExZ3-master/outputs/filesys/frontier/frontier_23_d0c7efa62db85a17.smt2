(set-logic ALL)
; Frontier Constraint ID: d0c7efa62db85a17
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1195)) (False)
(assert (not (= x 1195)))

; Query: ((== x 1196)) (False)
(assert (not (not (= x 1196))))

(check-sat)
(get-model)
